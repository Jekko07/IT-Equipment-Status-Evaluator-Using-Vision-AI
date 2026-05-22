import base64
import requests
import json
import sys

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:4b"  # Change if you're using a different name

def encode_image_to_base64(image_path):
    """Encodes an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded

def query_gemma3_vision(image_path, prompt=\
    "You are an automated IT inspection system. \
    Your task is to evaluate the IMAGE provided. \
    \
    DO NOT explain anything about code, scripts, or process. \
    DO NOT simulate or describe what you would do. \
    DO NOT give meta explanations. \
    \
    ONLY evaluate the image using the criteria below: \
    \
    Cable Management (0 or 1) \
    Workspace Cleanliness (0 or 1) \
    Equipment Condition (0 or 1) \
    \
    Compute total score out of 3. \
    \
    Output EXACTLY in this format: \
    Cable Management: X \
    Workspace Cleanliness: X \
    Equipment Condition: X \
    Total Score: X/3 \
    Final Evaluation: EXCELLENT or ACCEPTABLE or NEEDS IMPROVEMENT \
    Explanation: short explanation of the image only."):


    image_base64 = encode_image_to_base64(image_path)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "images": [image_base64],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "No response text returned.")

    except requests.RequestException as e:
        return f"Request failed: {e}"

def convert_to_score(text):
    text = text.lower()

    cable = 0
    clean = 0
    condition = 1  # assume working unless damage is mentioned

    
    # Cable management logic
    if any(word in text for word in ["neat", "organized", "tidy", "well-managed", "low clutter"]):
        cable = 1
    else:
        cable = 0

    # Cleanliness logic
    if any(word in text for word in ["clean", "clear", "minimal clutter"]):
        clean = 1
    else:
        clean = 0

    # Equipment condition logic
    if any(word in text for word in ["damage", "broken", "fault", "defective"]):
        condition = 0
    else:
        condition = 1


    total = cable + clean + condition

    if total == 3:
        evaluation = "EXCELLENT"
    elif total == 2:
        evaluation = "ACCEPTABLE"
    else:
        evaluation = "NEEDS IMPROVEMENT"

    return cable, clean, condition, total, evaluation

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python it_equipment_eval.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    insights = query_gemma3_vision(image_path)
    print("=== RAW AI OUTPUT ===")
    print(insights)

    # ✅ Structured scoring
    cable, clean, condition, total, evaluation = convert_to_score(insights)

    print("\n=== FINAL STRUCTURED OUTPUT ===")
    print(f"Cable Management: {cable}")
    print(f"Workspace Cleanliness: {clean}")
    print(f"Equipment Condition: {condition}")
    print(f"Total Score: {total}/3")
    print(f"Final Evaluation: {evaluation}")


    
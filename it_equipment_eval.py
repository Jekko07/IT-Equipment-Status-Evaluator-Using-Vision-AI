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
    "You are an IT equipment evaluator. Analyze the given image ONLY. \
    Do NOT explain the code or the script. \
    Evaluate the image based on the following criteria: \
    1. Cable management (1 point) \
    2. Workspace cleanliness (1 point) \
    3. Equipment condition (no visible damage) (1 point) \
    \
    Output format STRICTLY: \
    Cable Management: (0 or 1) \
    Workspace Cleanliness: (0 or 1) \
    Equipment Condition: (0 or 1) \
    Total Score: X/3 \
    Final Evaluation: EXCELLENT / ACCEPTABLE / NEEDS IMPROVEMENT \
    \
    Give a short explanation after the scores."):

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gemma3_vision_insight.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    insights = query_gemma3_vision(image_path)
    print("=== Insights Extracted ===")
    print(insights)
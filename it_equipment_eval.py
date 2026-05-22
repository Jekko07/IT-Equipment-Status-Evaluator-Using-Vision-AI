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
    "Evaluate this image of an IT workspace or equipment setup. \
    Criteria: \
    1. Proper cable management (1 point) \
    2. Clean and organized workspace (1 point) \
    3. Equipment appears functional with no visible damage (1 point) \
    Instructions: \
    - Give score per criterion (0 or 1) \
    - Compute total score out of 3 \
    - Provide final evaluation: \
        3 = EXCELLENT \
        2 = ACCEPTABLE \
        1 or below = NEEDS IMPROVEMENT \
    - Provide a short explanation."):

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
import os
import google.generativeai as genai
from google.cloud import vision

# Load the API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    raise ValueError("API key not found! Please provide a valid API key.")

# Vision API client for image recognition
vision_client = vision.ImageAnnotatorClient()

# Generative model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="You are a professional salesperson working at an eCommerce store called OutfitMe. "
                       "Recommend different outfits based on the user's input or image-based clothing."
)

history = []

def detect_clothing_in_image(image_path):
    """Use Google Cloud Vision API to detect clothing items in the image."""
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations

    clothing_items = [label.description for label in labels if label.description in ["Shirt", "Pants", "Jacket", "Dress", "Shoes"]]
    return clothing_items

print("Star: Hey there, I am Star. What can I do for you today?")
stop_word = "stop"

while True:
    user_input = input("You: ")

    if user_input.lower() == stop_word:
        break

    if user_input.startswith('image:'):
        # Simulate image processing (in actual implementation, upload image or provide image URL)
        image_path = user_input.replace('image:', '').strip()
        clothing_items = detect_clothing_in_image(image_path)
        user_input = f"The user is wearing: {', '.join(clothing_items)}. Can you recommend matching outfits?"

    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(user_input)

    model_response = response.text
    print(f"Star: {model_response}\n")

    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})

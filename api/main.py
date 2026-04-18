import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
# Load your API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Set GEMINI_API_KEY in your env!")

# Use the new GenAI client
client = genai.Client(api_key=api_key)

print("Available models (supporting generateContent):\n")
for model in client.models.list():
    for action in model.supported_actions:
        if action == "generateContent":
            print(f"  → {model.name}")
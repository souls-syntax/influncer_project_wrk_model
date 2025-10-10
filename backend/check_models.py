import google.generativeai as genai
from config import GEMINI_API_KEY

try:
    genai.configure(api_key=GEMINI_API_KEY)

    print("Successfully connected to Google AI. Available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")

except Exception as e:
    print(f"\nAn error occurred: {type(e).__name__}: {e}")
    print("\nPlease double-check your GEMINI_API_KEY in config.py and ensure the library is installed correctly with 'pip install google-generativeai'.")
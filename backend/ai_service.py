# import json
# import sys
# # Sahi import tareeka, taaki future mein problem na ho
# import google.generativeai as genai
# from google.generativeai import types
# from config import GEMINI_API_KEY

# # Step 1: Client ko bilkul aapke prototype ki tarah initialize karna
# try:
#     if not GEMINI_API_KEY or "YOUR_GEMINI_API_KEY_HERE" in GEMINI_API_KEY:
#         print("FATAL ERROR: GEMINI_API_KEY sahi se config.py mein set nahi hai.")
#         sys.exit(1)
    
#     # Hum 'genai.configure' ka istemal karenge jo ki standard tareeka hai
#     genai.configure(api_key=GEMINI_API_KEY)

# except Exception as e:
#     print(f"FATAL ERROR: GenAI client initialize nahi ho paaya. Apni API Key check karein. Error: {e}")
#     sys.exit(1)

# # Step 2: Aapke prototype se liya gaya 'schema'
# RECOMMENDATION_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "primary_niche": {
#             "type": "string",
#             "description": "The most precise niche (e.g., 'Vegan Fitness', 'DIY Home Repair')."
#         },
#         "brand_safety_score_1_to_10": {
#             "type": "integer",
#             "description": "Score from 1 (High Risk/Controversial) to 10 (Extremely Safe/Professional)."
#         },
#         "risk_summary": {
#             "type": "string",
#             "description": "A brief, 1-sentence summary of the main risk factors (e.g., 'High engagement but inconsistent posting schedule' or 'Excellent fit, professional contact provided')."
#         },
#         "keywords": {
#             "type": "array",
#             "description": "5-7 specific keywords that describe the influencer's content style and audience interests.",
#             "items": {"type": "string"} 
#         },
#         "recommendation": {
#             "type": "string",
#             "description": "A final verdict: 'Strongly Recommended', 'Recommended with caution', or 'Not Recommended'."
#         }
#     },
#     "required": ["primary_niche", "brand_safety_score_1_to_10", "risk_summary", "keywords", "recommendation"]
# }

# # Step 3: Function ka naam project ke hisaab se rakhna ('classify_influencer')
# def classify_influencer(ai_prompt_text: str):
#     """
#     Influencer ke data ko GenAI ko bhejkar Brand Safety aur Recommendation analysis karta hai.
#     """
    
#     # Model ko initialize karne ka naya aur standard tareeka
#     model = genai.GenerativeModel(
#       # Aapke prototype wala model, jo aapke account mein uplabdh hai
#       'gemini-2.5-flash', 
#       system_instruction=(
#             "You are an expert Brand Safety and Influencer Vetting Analyst. "
#             "Analyze the provided technical and textual data to determine the influencer's suitability for a business advertisement partnership. "
#             "Focus heavily on the engagement rate, content consistency, and tone of the content/tags. "
#             "Your response MUST be a valid JSON object matching the provided schema."
#         )
#     )

#     prompt = f"Analyze the following influencer profile data and provide a detailed brand recommendation:\n\n---\n{ai_prompt_text}\n---"

#     try:
#         # API call karne ka standard tareeka
#         response = model.generate_content(
#             prompt,
#             generation_config=genai.types.GenerationConfig(
#                 response_mime_type="application/json",
#                 response_schema=RECOMMENDATION_SCHEMA
#             )
#         )
        
#         return json.loads(response.text)
        
#     except Exception as e:
#         print(f"  [GenAI EXCEPTION] Classification failed: {type(e).__name__}: {e}")
#         # Error aane par hum AI ka raw response bhi print karenge
#         if 'response' in locals() and hasattr(response, 'text'):
#             print(f"  [GenAI RAW RESPONSE]: {response.text}")
#         return {
#             "primary_niche": "AI_Failed",
#             "brand_safety_score_1_to_10": 0,
#             "risk_summary": f"AI classification failed due to: {e}",
#             "keywords": [],
#             "recommendation": "Not Recommended"
#         }
import json
import time
import random

def classify_influencer(ai_prompt_text: str):
    """
    Yeh ek MOCK (nakli) AI service hai.
    Yeh GenAI jaisa hi ek realistic, random dummy JSON response deta hai
    taaki project chalta rahe aur data ajeeb na lage.
    """
    print("  [MOCK AI] Analyzing... (returning realistic temporary data)")
    
    # Hum yahan 1 second ka delay daal rahe hain taaki yeh asli AI jaisa lage
    time.sleep(1) 
    
    # Alag-alag scenarios ke liye kuch dummy data
    niches = ["Gaming Commentary", "DIY Crafts", "Fitness & Nutrition", "Tech Reviews", "Street Food Vlogs"]
    recommendations = ["Strongly Recommended", "Recommended with caution", "Not Recommended"]
    
    # Ek random, realistic response banayein
    dummy_response = {
        "primary_niche": random.choice(niches),
        "brand_safety_score_1_to_10": random.randint(5, 10),
        "risk_summary": "Content is generally safe, with some inconsistent posting.",
        "keywords": ["entertainment", random.choice(niches).lower(), "influencer", "vlogger"],
        "recommendation": random.choice(recommendations)
    }
    
    return dummy_response
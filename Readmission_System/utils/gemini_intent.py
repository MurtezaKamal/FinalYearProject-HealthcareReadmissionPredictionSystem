# utils/gemini_intent.py
import google.generativeai as genai
import os

api_key = os.getenv("GOOGLE_API_KEY")  
genai.configure(api_key=api_key)

# Gemini model (can be imported anywhere)
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- Intent Extraction ---------------- #
def get_user_intent(query):
    system_prompt = """
    You are an AI that extracts intent from user queries about a hospital readmission prediction system.
    Based on the query, return one of the following keywords ONLY (lowercase, no explanation):

    - get_top_correlation
    - get_negative_correlation
    - get_best_model
    - get_model_ranking
    - get_top_features
    - get_readmission_rate
    - unknown
    """

    try:
        result = model.generate_content(f"{system_prompt}\n\nUser query: {query}")
        return result.text.strip().lower()
    except Exception as e:
        return "unknown"

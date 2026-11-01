import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
key = os.environ.get("GEMINI_API_KEY", "")
print("Key found:", bool(key), "| length:", len(key))
client = genai.Client(api_key=key)

for model in ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3.5-flash"]:
    try:
        r = client.models.generate_content(model=model, contents="Say OK")
        print(model, "WORKS:", (r.text or "").strip()[:20])
    except Exception as e:
        print(model, "FAILED:", type(e).__name__, getattr(e, "code", ""), str(e)[:250])
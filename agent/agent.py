import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Tries models in this order. If one is busy or missing, it moves to the next.
_candidates = [
    os.getenv("GEMINI_MODEL"),
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.5-flash",
]
MODELS = []
for m in _candidates:
    if m and m not in MODELS:
        MODELS.append(m)

HOSPITALS = {
    "bhubaneswar": ["AIIMS Bhubaneswar", "Capital Hospital", "SUM Ultimate Medicare"],
    "cuttack": ["SCB Medical College and Hospital", "Cuttack City Hospital"],
    "puri": ["District Headquarters Hospital, Puri"],
    "sambalpur": ["VIMSAR, Burla", "District Headquarters Hospital, Sambalpur"],
    "berhampur": ["MKCG Medical College and Hospital"],
    "rourkela": ["Ispat General Hospital"],
    "balasore": ["District Headquarters Hospital, Balasore"],
    "ganjam": ["MKCG Medical College and Hospital, Berhampur"],
    "mayurbhanj": ["District Headquarters Hospital, Baripada"],
}

EMERGENCY_WORDS = [
    "chest pain", "can't breathe", "cannot breathe", "difficulty breathing",
    "unconscious", "fainted",
    "ଛାତି ବିନ୍ଧ", "ନିଶ୍ୱାସ", "ବେହୋସ",
    "सीने में दर्द", "सांस", "बेहोश",
]

EMERGENCY_MSG = (
    "EMERGENCY: Call 108 now or go to the nearest hospital immediately.\n"
    "ଜରୁରୀକାଳୀନ: ଏବେ 108 କୁ କଲ୍ କରନ୍ତୁ କିମ୍ବା ନିକଟତମ ହସ୍ପିଟାଲକୁ ତୁରନ୍ତ ଯାଆନ୍ତୁ।\n"
    "आपातकाल: अभी 108 पर कॉल करें या तुरंत नजदीकी अस्पताल जाएं।"
)

SYSTEM = """You are Arogya Mitra, a health guidance assistant for rural Odisha.
- Reply in the same language the patient wrote in (Odia script for Odia, Hindi for Hindi, English for English). Use simple words.
- Never diagnose. Say "possible causes". Never name medicines or doses.
- If duration or severity is unknown, ask ONE short follow-up question.
- Safe advice only: rest, fluids, ORS, light food, when to see a doctor or PHC.
- Call find_hospitals ONLY when symptoms are serious, have lasted several days, or the patient asks for a hospital. Do not list hospitals for mild symptoms.
- For anything serious, tell them to call 108 (emergency).
- End with a one-line reminder that this is guidance, not a diagnosis."""


def find_hospitals(district: str) -> list:
    """Return hospitals for an Odisha district."""
    return HOSPITALS.get(district.strip().lower(), ["Hospital list for this district is not available yet. Please ask a local health worker."])


def is_emergency(text: str) -> bool:
    t = text.lower()
    return any(w in t for w in EMERGENCY_WORDS)


def call_model(history: list):
    """Try each model, with short retries, until one answers."""
    last_error = None
    for model in MODELS:
        for attempt in range(2):
            try:
                return client.models.generate_content(
                    model=model,
                    contents=history,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM, tools=[find_hospitals]
                    ),
                )
            except Exception as e:
                last_error = e
                time.sleep(2 * (attempt + 1))
    raise last_error


def chat(history: list, user_text: str, district: str) -> str:
    # Safety check runs in plain code, before the model.
    if is_emergency(user_text):
        return EMERGENCY_MSG

    history.append(
        types.Content(role="user", parts=[types.Part(text=f"[District: {district}] {user_text}")])
    )
    try:
        response = call_model(history)
    except Exception:
        history.pop()  # remove the unanswered message
        raise
    history.append(response.candidates[0].content)
    return response.text


if __name__ == "__main__":
    history = []
    district = input("District (e.g. Cuttack): ").strip() or "Bhubaneswar"
    print("Type 'quit' to stop.")
    while True:
        text = input("You: ").strip()
        if text.lower() in ("quit", "exit"):
            break
        try:
            print("Arogya Mitra:", chat(history, text, district))
        except Exception as e:
            print("Sorry, the AI is busy right now. Please try again in a minute.", type(e).__name__)
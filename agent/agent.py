import csv
import re
import unicodedata
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

# ---------------------------------------------------------------------------
# Hospital data is read from data/odisha/hospitals.csv
# ---------------------------------------------------------------------------
DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "odisha", "hospitals.csv"
)


def load_hospitals():
    hospitals = {}
    try:
        with open(DATA_FILE, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                key = (row.get("district") or "").strip().lower()
                if key:
                    hospitals.setdefault(key, []).append(row)
    except FileNotFoundError:
        pass
    return hospitals


HOSPITALS = load_hospitals()

EMERGENCY_WORDS = [
    # English
    "chest pain", "pain in chest", "can't breathe", "cannot breathe",
    "difficulty breathing", "trouble breathing", "short of breath",
    "unconscious", "fainted", "not responding", "seizure", "fits",
    "vomiting blood", "blood in vomit", "heavy bleeding", "snake bite",
    "poison",
    # Odia
    "ଛାତି ବିନ୍ଧ", "ଛାତିରେ ଯନ୍ତ୍ରଣା", "ନିଶ୍ୱାସ ନେବାକୁ କଷ୍ଟ", "ଶ୍ୱାସକଷ୍ଟ",
    "ବେହୋସ", "ଅଚେତ", "ରକ୍ତ ବାନ୍ତି", "ସାପ କାମୁଡ଼ା",
         "ସାପ କାମୁଡ",   
    
    # Hindi
    "सीने में दर्द", "सांस लेने में तकलीफ", "सांस फूल", "बेहोश",
    "दौरा", "खून की उल्टी", "सांप ने काटा", "ज़हर", "जहर",
    # Odia/Hindi in English letters
    "chhati bindh", "behosh", "saans lene mein", "sapa kamuda",
        "chhati bindhuchi", "chhati bindhu", "chati bindhuchi", "chhati bindha",
    "sapa kamudichi", "behosha",
]

EMERGENCY_MSG = (
    "🚨 **EMERGENCY:** Call 108 now or go to the nearest hospital immediately.\n\n"
    "🚨 **ଜରୁରୀକାଳୀନ:** ଏବେ 108 କୁ କଲ୍ କରନ୍ତୁ କିମ୍ବା ନିକଟତମ ହସ୍ପିଟାଲକୁ ତୁରନ୍ତ ଯାଆନ୍ତୁ।\n\n"
    "🚨 **आपातकाल:** अभी 108 पर कॉल करें या तुरंत नजदीकी अस्पताल जाएं।"
)

SYSTEM = """You are Arogya Mitra, a health guidance assistant for rural Odisha.
- Reply in the same language the patient wrote in (Odia script for Odia, Hindi for Hindi, English for English). Use simple words.
- Never diagnose. Say "possible causes". Never name medicines or doses.
- If duration or severity is unknown, ask ONE short follow-up question.
- Safe advice only: rest, fluids, ORS, light food, when to see a doctor or PHC.
- Call find_hospitals ONLY when symptoms are serious, have lasted several days, or the patient asks for a hospital. Do not list hospitals for mild symptoms.
- When you list hospitals, use only what find_hospitals returns. Never invent hospital names or phone numbers. Tell the patient to confirm details before travelling.
- For anything serious, tell them to call 108 (emergency).
- When replying in Odia, use simple spoken Odia that a village resident would understand. Avoid bookish or Sanskrit-heavy words. Do not add English words in brackets.
- Keep replies short: at most 5 bullet points.
- Format: write every bullet point on its own new line starting with "- ", and leave a blank line between sections.
- End with a one-line reminder that this is guidance, not a diagnosis."""


def find_hospitals(district: str) -> list:
    """Return hospitals for an Odisha district."""
    rows = HOSPITALS.get(district.strip().lower())
    if not rows:
        return ["Hospital list for this district is not available yet. Please ask a local health worker."]
    result = []
    for r in rows:
        line = f'{r["name"]} ({r["type"]})'
        phone = (r.get("phone") or "").strip()
        if phone:
            line += f", phone: {phone}"
        result.append(line)
    return result


NEGATIONS = r"(?:no|not|without|never|gone)"


def is_emergency(text: str) -> bool:
    t = unicodedata.normalize("NFC", text.lower())
    for w in EMERGENCY_WORDS:
        w = unicodedata.normalize("NFC", w.lower())
        if w.isascii():
            # English phrases: whole words only, and skip if just negated
            for m in re.finditer(r"\b" + re.escape(w) + r"\b", t):
                before = t[: m.start()]
                if not re.search(r"\b" + NEGATIONS + r"\s+(?:\w+\s+)?$", before):
                    return True
        elif w in t:
            # Odia and Hindi phrases: plain match
            return True
    return False

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
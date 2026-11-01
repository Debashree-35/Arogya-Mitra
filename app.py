import csv
import os
from datetime import datetime

import streamlit as st

try:
    from agent.agent import chat
    AGENT_OK = True
except Exception:
    AGENT_OK = False

st.set_page_config(page_title="Arogya Mitra | Pilot: Odisha", page_icon="🩺", layout="wide")

st.markdown("""
<style>
.stButton>button {background-color: #FF4B4B; color: white; font-weight: bold; border-radius: 10px; padding: 10px 20px;}
</style>
""", unsafe_allow_html=True)

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "odisha", "hospitals.csv"
)


@st.cache_data
def load_hospital_rows():
    try:
        with open(DATA_FILE, encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


# ---------------------------------------------------------------------------
# Content for the rule-based Symptom Checker tab.
# No medicine names or doses on purpose. Odia and Hindi text should be
# reviewed by a native speaker.
# ---------------------------------------------------------------------------
CONTENT = {
    "English": {
        "emergency": "🚨 EMERGENCY: Call 108 now or go to the nearest hospital immediately.",
        "nomed": "Do not take medicines without asking a doctor or pharmacist.",
        "general": "General illness. Please consult a doctor or visit your nearest PHC.",
        "fever": {
            "title": "Possible causes: viral fever, dengue or malaria (cannot be confirmed without tests)",
            "care": "Rest, drink plenty of fluids and ORS, eat light food like khichdi and dalma.",
            "extra": "Dengue and malaria tests may be needed, especially if fever lasts more than 3 days. Visit a PHC if not improving in 2 days.",
        },
        "stomach": {
            "title": "Possible cause: stomach infection (gastroenteritis)",
            "care": "Take ORS in small frequent sips, eat light food, drink clean boiled water.",
            "extra": "Go to a hospital if there is blood in stool, signs of severe dehydration, or vomiting that does not stop.",
        },
        "cold": {
            "title": "Possible cause: common cold or flu",
            "care": "Steam inhalation, warm water, rest, tulsi or ginger tea.",
            "extra": "See a doctor if breathing becomes difficult or fever lasts more than 3 days.",
        },
        "head": {
            "title": "Possible cause: tension headache, dehydration or migraine",
            "care": "Rest in a quiet dark room and drink water.",
            "extra": "See a doctor urgently for a sudden severe headache, repeated vomiting, or vision problems.",
        },
    },
    "Odia (ଓଡ଼ିଆ)": {
        "emergency": "🚨 ଜରୁରୀକାଳୀନ: ଏବେ 108 କୁ କଲ୍ କରନ୍ତୁ କିମ୍ବା ନିକଟତମ ହସ୍ପିଟାଲକୁ ତୁରନ୍ତ ଯାଆନ୍ତୁ।",
        "nomed": "ଡାକ୍ତର କିମ୍ବା ଫାର୍ମାସିଷ୍ଟଙ୍କୁ ପଚାରିବା ବିନା ଔଷଧ ଖାଆନ୍ତୁ ନାହିଁ।",
        "general": "ସାଧାରଣ ଅସୁସ୍ଥତା। ଦୟାକରି ଡାକ୍ତରଙ୍କ ପରାମର୍ଶ ନିଅନ୍ତୁ କିମ୍ବା ନିକଟତମ PHC କୁ ଯାଆନ୍ତୁ।",
        "fever": {
            "title": "ସମ୍ଭାବ୍ୟ କାରଣ: ଭାଇରାଲ ଜ୍ୱର, ଡେଙ୍ଗୁ କିମ୍ବା ମ୍ୟାଲେରିଆ (ପରୀକ୍ଷା ବିନା ନିଶ୍ଚିତ ହୋଇପାରିବ ନାହିଁ)",
            "care": "ବିଶ୍ରାମ ନିଅନ୍ତୁ, ଅଧିକ ପାଣି ଓ ORS ପିଅନ୍ତୁ, ଖିଚଡ଼ି ଓ ଡାଲମା ପରି ହାଲୁକା ଖାଦ୍ୟ ଖାଆନ୍ତୁ।",
            "extra": "ଜ୍ୱର 3 ଦିନରୁ ଅଧିକ ରହିଲେ ଡେଙ୍ଗୁ ଓ ମ୍ୟାଲେରିଆ ପରୀକ୍ଷା ଆବଶ୍ୟକ ହୋଇପାରେ। 2 ଦିନରେ ଭଲ ନ ହେଲେ PHC ଯାଆନ୍ତୁ।",
        },
        "stomach": {
            "title": "ସମ୍ଭାବ୍ୟ କାରଣ: ପେଟ ସଂକ୍ରମଣ (ଗ୍ୟାଷ୍ଟ୍ରୋଏଣ୍ଟେରାଇଟିସ୍)",
            "care": "ଅଳ୍ପ ଅଳ୍ପ କରି ବାରମ୍ବାର ORS ପିଅନ୍ତୁ, ହାଲୁକା ଖାଦ୍ୟ ଖାଆନ୍ତୁ, ଫୁଟା ପାଣି ପିଅନ୍ତୁ।",
            "extra": "ଝାଡ଼ାରେ ରକ୍ତ ଥିଲେ, ଅତ୍ୟଧିକ ପାଣି ଅଭାବର ଲକ୍ଷଣ ଥିଲେ, କିମ୍ବା ବାନ୍ତି ବନ୍ଦ ନ ହେଲେ ହସ୍ପିଟାଲ ଯାଆନ୍ତୁ।",
        },
        "cold": {
            "title": "ସମ୍ଭାବ୍ୟ କାରଣ: ସାଧାରଣ ଥଣ୍ଡା କିମ୍ବା ଫ୍ଲୁ",
            "care": "ଭାପ ନିଅନ୍ତୁ, ଗରମ ପାଣି ପିଅନ୍ତୁ, ବିଶ୍ରାମ ନିଅନ୍ତୁ, ତୁଳସୀ କିମ୍ବା ଅଦା ଚା ପିଅନ୍ତୁ।",
            "extra": "ନିଶ୍ୱାସ ନେବାରେ କଷ୍ଟ ହେଲେ କିମ୍ବା ଜ୍ୱର 3 ଦିନରୁ ଅଧିକ ରହିଲେ ଡାକ୍ତର ଦେଖାନ୍ତୁ।",
        },
        "head": {
            "title": "ସମ୍ଭାବ୍ୟ କାରଣ: ଚାପଜନିତ ମୁଣ୍ଡ ବିନ୍ଧା, ପାଣି ଅଭାବ କିମ୍ବା ମାଇଗ୍ରେନ",
            "care": "ଶାନ୍ତ ଅନ୍ଧାର ଘରେ ବିଶ୍ରାମ ନିଅନ୍ତୁ ଓ ପାଣି ପିଅନ୍ତୁ।",
            "extra": "ହଠାତ୍ ତୀବ୍ର ମୁଣ୍ଡ ବିନ୍ଧା, ବାରମ୍ବାର ବାନ୍ତି, କିମ୍ବା ଦୃଷ୍ଟି ସମସ୍ୟା ହେଲେ ତୁରନ୍ତ ଡାକ୍ତର ଦେଖାନ୍ତୁ।",
        },
    },
    "Hindi": {
        "emergency": "🚨 आपातकाल: अभी 108 पर कॉल करें या तुरंत नजदीकी अस्पताल जाएं।",
        "nomed": "डॉक्टर या फार्मासिस्ट से पूछे बिना दवा न लें।",
        "general": "सामान्य बीमारी। कृपया डॉक्टर से सलाह लें या नजदीकी PHC जाएं।",
        "fever": {
            "title": "संभावित कारण: वायरल बुखार, डेंगू या मलेरिया (जाँच के बिना पुष्टि नहीं हो सकती)",
            "care": "आराम करें, खूब पानी और ORS पिएं, खिचड़ी और दालमा जैसा हल्का खाना खाएं।",
            "extra": "बुखार 3 दिन से ज्यादा रहे तो डेंगू और मलेरिया की जाँच की जरूरत हो सकती है। 2 दिन में ठीक न हो तो PHC जाएं।",
        },
        "stomach": {
            "title": "संभावित कारण: पेट का संक्रमण (गैस्ट्रोएंटेराइटिस)",
            "care": "थोड़ा-थोड़ा करके बार-बार ORS पिएं, हल्का खाना खाएं, उबला हुआ साफ पानी पिएं।",
            "extra": "मल में खून हो, पानी की गंभीर कमी के लक्षण हों, या उल्टी न रुके तो अस्पताल जाएं।",
        },
        "cold": {
            "title": "संभावित कारण: सामान्य सर्दी या फ्लू",
            "care": "भाप लें, गर्म पानी पिएं, आराम करें, तुलसी या अदरक की चाय पिएं।",
            "extra": "सांस लेने में तकलीफ हो या बुखार 3 दिन से ज्यादा रहे तो डॉक्टर को दिखाएं।",
        },
        "head": {
            "title": "संभावित कारण: तनाव वाला सिरदर्द, पानी की कमी या माइग्रेन",
            "care": "शांत अंधेरे कमरे में आराम करें और पानी पिएं।",
            "extra": "अचानक तेज सिरदर्द, बार-बार उल्टी, या देखने में दिक्कत हो तो तुरंत डॉक्टर को दिखाएं।",
        },
    },
}

RED_FLAGS = {"Chest Pain", "Breathing Difficulty"}

# ---------------------------------------------------------------------------
# Header and sidebar
# ---------------------------------------------------------------------------
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🩺 Arogya Mitra")
    st.subheader("Health guidance for rural communities | ଗ୍ରାମୀଣ ସ୍ୱାସ୍ଥ୍ୟ ସେବା")
    st.caption("Pilot: Odisha. Check symptoms, find nearby hospitals, and get basic care guidance.")
with col2:
    st.caption(f"📅 {datetime.now().strftime('%d %B %Y')}")

st.divider()

st.sidebar.title("👤 Patient Profile")
name = st.sidebar.text_input("Full Name", "")
age = st.sidebar.number_input("Age", 1, 120, 25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
district = st.sidebar.selectbox(
    "District",
    ["Bhubaneswar", "Cuttack", "Puri", "Ganjam", "Berhampur", "Sambalpur",
     "Rourkela", "Balasore", "Mayurbhanj", "Other"],
)
language = st.sidebar.radio("Language / ଭାଷା", ["English", "Odia (ଓଡ଼ିଆ)", "Hindi"])
st.sidebar.success(f"✅ {district} | {language}")
st.sidebar.caption("The language setting changes the Symptom Checker. The AI Assistant replies in the language you write in.")

T = CONTENT[language]

tab_check, tab_ai, tab_hosp, tab_about = st.tabs(
    ["🩺 Symptom Checker", "🤖 AI Assistant", "🏥 Hospital Finder", "ℹ️ About"]
)

# ---------------------------------------------------------------------------
# Tab: Symptom Checker (rule-based)
# ---------------------------------------------------------------------------
with tab_check:
    st.subheader(
        "Step 1: Select Symptoms" if language == "English"
        else "ପଦକ୍ଷେପ 1: ଲକ୍ଷଣ ବାଛନ୍ତୁ" if language.startswith("Odia")
        else "चरण 1: लक्षण चुनें"
    )
    symptoms = st.multiselect(
        "Choose all symptoms you have:",
        ["Fever", "Cough", "Cold", "Headache", "Body Pain", "Stomach Pain", "Diarrhea",
         "Vomiting", "Sore Throat", "Fatigue", "Breathing Difficulty", "Chest Pain",
         "Dizziness", "Skin Rash"],
        default=["Fever", "Cough"],
    )
    duration = st.slider("Duration (days)", 1, 14, 2)
    severity = st.select_slider("Severity", options=["Mild", "Moderate", "Severe"], value="Moderate")

    if st.button("🔍 Check Symptoms", type="primary"):
        if not symptoms:
            st.warning("Please select at least one symptom.")
        else:
            # Rule-based urgency. Thresholds are placeholders and must be
            # reviewed by a medical professional before real-world use.
            if RED_FLAGS & set(symptoms):
                urgency = "emergency"
            elif severity == "Severe" or duration >= 5 or len(symptoms) >= 5:
                urgency = "doctor24"
            else:
                urgency = "home"

            if urgency == "emergency":
                st.error(T["emergency"])
            else:
                if urgency == "doctor24":
                    st.warning("⚠️ Please visit a doctor within 24 hours.")
                else:
                    st.success("Home care may be enough. Watch your symptoms and see a doctor if they get worse.")

                if "Fever" in symptoms and ("Cough" in symptoms or "Body Pain" in symptoms):
                    cond = "fever"
                elif "Diarrhea" in symptoms or "Stomach Pain" in symptoms or "Vomiting" in symptoms:
                    cond = "stomach"
                elif "Cold" in symptoms or "Sore Throat" in symptoms or "Cough" in symptoms:
                    cond = "cold"
                elif "Headache" in symptoms:
                    cond = "head"
                else:
                    cond = None

                if cond:
                    st.info(T[cond]["title"])
                    st.write(T[cond]["care"])
                    st.write(T[cond]["extra"])
                else:
                    st.info(T["general"])
                st.caption(T["nomed"])

            st.divider()
            st.write("**📋 Summary to show a doctor or health worker:**")
            st.code(
                f"Patient: {name or 'N/A'} | Age: {age} | Gender: {gender} | District: {district}\n"
                f"Symptoms: {', '.join(symptoms)}\n"
                f"Duration: {duration} days | Severity: {severity}\n"
                f"Urgency (rule-based): {urgency}"
            )

# ---------------------------------------------------------------------------
# Tab: AI Assistant
# ---------------------------------------------------------------------------
with tab_ai:
    st.subheader("🤖 AI Health Assistant")
    st.caption("Type in Odia, Hindi or English. Guidance only, not a diagnosis.")
    if not AGENT_OK:
        st.warning("The AI assistant is not configured yet.")
    else:
        if "history" not in st.session_state:
            st.session_state.history = []
            st.session_state.messages = []
        if st.button("🗑️ Clear chat"):
            st.session_state.history = []
            st.session_state.messages = []
            st.rerun()
        # Messages live in a fixed-height box, so the input below never moves.
        chat_box = st.container(height=450, border=True)
        prompt = st.chat_input("Describe your problem...")
        with chat_box:
            if not st.session_state.messages and not prompt:
                st.caption("Your conversation will appear here. Type your problem below.")
            for m in st.session_state.messages:
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])
            if prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            reply = chat(st.session_state.history, prompt, district)
                        except Exception:
                            reply = "Sorry, the AI is busy right now. Please try again in a minute."
                    st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

# ---------------------------------------------------------------------------
# Tab: Hospital Finder (reads data/odisha/hospitals.csv)
# ---------------------------------------------------------------------------
with tab_hosp:
    st.subheader("🏥 Hospitals in your district")
    rows = [r for r in load_hospital_rows() if r["district"].strip().lower() == district.lower()]
    if rows:
        for r in rows:
            st.write(f"✅ **{r['name']}** ({r['type']})")
            phone = (r.get("phone") or "").strip()
            if phone:
                st.caption(f"Phone: {phone}")
            if (r.get("source") or "").strip():
                st.caption(f"Source: {r['source']}")
    else:
        st.info("Verified hospital data for this district is not available yet. Please ask a local health worker or visit your nearest PHC.")
    st.caption("Names were checked against official government pages in October 2026. Please confirm details before travelling.")
    st.success("🚨 Emergency ambulance: **108**")

# ---------------------------------------------------------------------------
# Tab: About
# ---------------------------------------------------------------------------
with tab_about:
    st.subheader("About Arogya Mitra")
    st.write(
        "Arogya Mitra is an open-source project built for the Code for a Billion: "
        "Bharat Agentic-AI Hackathon 2026. This pilot focuses on Odisha, with "
        "English, Odia and Hindi support."
    )
    st.write("**Status:** early prototype. Guidance is not clinically validated and has not been reviewed by a doctor.")
    st.write("**How it works:** emergency words are checked first in plain code, then an AI backup check runs, then the AI assistant answers and looks up hospitals from a verified data file.")
    st.write("**Limits:** hospital data covers a few districts only, and the AI service can be busy or wrong.")

st.divider()
st.caption(
    "⚠️ Disclaimer: General awareness only. This is not a medical diagnosis and does not replace a doctor. "
    "In an emergency call 108."
)
st.caption("Built for Code for a Billion: Bharat Agentic-AI Hackathon 2026.")
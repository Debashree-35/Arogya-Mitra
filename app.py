import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Arogya Mitra | Pilot: Odisha", page_icon="🩺", layout="wide")

st.markdown("""
<style>
.stButton>button {background-color: #FF4B4B; color: white; font-weight: bold; border-radius: 10px; padding: 10px 20px;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Content per language.
# NOTE: Odia and Hindi text should be reviewed by a native speaker.
# NOTE: No medicine names or dosages on purpose. A rule-based app must not
#       prescribe. Replace with doctor-reviewed content later.
# ---------------------------------------------------------------------------
CONTENT = {
    "English": {
        "emergency": "🚨 EMERGENCY: Call 108 now or go to the nearest hospital immediately.",
        "nomed": "Do not take medicines without asking a doctor or pharmacist.",
        "general": "General illness. Please consult a doctor, or call the 104 health helpline.",
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
        "greeting": "Namaskar! I am Arogya Mitra. Tell me your symptoms.",
        "fallback": "I did not understand. Please use the Symptom Checker tab, or call 104.",
    },
    "Odia (ଓଡ଼ିଆ)": {
        "emergency": "🚨 ଜରୁରୀକାଳୀନ: ଏବେ 108 କୁ କଲ୍ କରନ୍ତୁ କିମ୍ବା ନିକଟତମ ହସ୍ପିଟାଲକୁ ତୁରନ୍ତ ଯାଆନ୍ତୁ।",
        "nomed": "ଡାକ୍ତର କିମ୍ବା ଫାର୍ମାସିଷ୍ଟଙ୍କୁ ପଚାରିବା ବିନା ଔଷଧ ଖାଆନ୍ତୁ ନାହିଁ।",
        "general": "ସାଧାରଣ ଅସୁସ୍ଥତା। ଦୟାକରି ଡାକ୍ତରଙ୍କ ପରାମର୍ଶ ନିଅନ୍ତୁ, କିମ୍ବା 104 ହେଲ୍ପଲାଇନକୁ କଲ୍ କରନ୍ତୁ।",
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
        "greeting": "ନମସ୍କାର! ମୁଁ ଆରୋଗ୍ୟ ମିତ୍ର। ଆପଣଙ୍କ ଲକ୍ଷଣ କୁହନ୍ତୁ।",
        "fallback": "ମୁଁ ବୁଝିପାରିଲି ନାହିଁ। ଦୟାକରି ଲକ୍ଷଣ ଯାଞ୍ଚ ଟ୍ୟାବ୍ ବ୍ୟବହାର କରନ୍ତୁ, କିମ୍ବା 104 କୁ କଲ୍ କରନ୍ତୁ।",
    },
    "Hindi": {
        "emergency": "🚨 आपातकाल: अभी 108 पर कॉल करें या तुरंत नजदीकी अस्पताल जाएं।",
        "nomed": "डॉक्टर या फार्मासिस्ट से पूछे बिना दवा न लें।",
        "general": "सामान्य बीमारी। कृपया डॉक्टर से सलाह लें, या 104 हेल्पलाइन पर कॉल करें।",
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
        "greeting": "नमस्कार! मैं आरोग्य मित्र हूँ। अपने लक्षण बताइए।",
        "fallback": "मैं समझ नहीं पाया। कृपया लक्षण जाँच टैब इस्तेमाल करें, या 104 पर कॉल करें।",
    },
}

CHAT_KEYWORDS = {
    "fever": ["fever", "jwara", "jara", "joro", "bukhar", "ଜ୍ୱର", "बुखार"],
    "head": ["head", "munda", "sir", "ମୁଣ୍ଡ", "सिर"],
    "cold": ["cold", "cough", "thanda", "kasa", "ଥଣ୍ଡା", "सर्दी", "खांसी"],
    "stomach": ["stomach", "pet", "jhara", "diarrhea", "ପେଟ", "पेट"],
}
EMERGENCY_KEYWORDS = ["chest pain", "breathing", "can't breathe", "unconscious", "ଛାତି ବିନ୍ଧା", "सीने में दर्द"]
RED_FLAGS = {"Chest Pain", "Breathing Difficulty"}

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🩺 Arogya Mitra")
    st.subheader("Health guidance for rural communities | ଗ୍ରାମୀଣ ସ୍ୱାସ୍ଥ୍ୟ ସେବା")
    st.caption("Pilot: Odisha. Check symptoms, find nearby hospitals, and get basic care guidance.")
with col2:
    st.caption(f"📅 {datetime.now().strftime('%d %B %Y')}")

st.divider()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title("👤 Patient Profile")
name = st.sidebar.text_input("Full Name", "")
age = st.sidebar.number_input("Age", 1, 120, 25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
district = st.sidebar.selectbox(
    "District",
    ["Bhubaneswar", "Cuttack", "Puri", "Sambalpur", "Berhampur", "Rourkela",
     "Balasore", "Ganjam", "Mayurbhanj", "Other"],
)
language = st.sidebar.radio("Language / ଭାଷା", ["English", "Odia (ଓଡ଼ିଆ)", "Hindi"])
st.sidebar.success(f"✅ {district} | {language}")

T = CONTENT[language]

tab1, tab2, tab3, tab4 = st.tabs(
    ["🩺 Symptom Checker", "💬 Quick Help", "🏥 Hospital Finder", "ℹ️ About"]
)

# ---------------------------------------------------------------------------
# Tab 1: Symptom checker (rule-based)
# ---------------------------------------------------------------------------
with tab1:
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
# Tab 2: Quick help (keyword matching, not an LLM yet)
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("💬 Quick Help")
    st.caption("Keyword-based answers for now. A conversational AI agent is being added.")
    q = st.text_input("Describe your problem:")
    if st.button("Ask"):
        qq = q.lower().strip()
        if not qq:
            st.warning("Please type your question.")
        elif any(w in qq for w in EMERGENCY_KEYWORDS):
            st.error(T["emergency"])
        else:
            matched = next((c for c, words in CHAT_KEYWORDS.items() if any(w in qq for w in words)), None)
            if matched:
                st.success(f"🤖 {T[matched]['title']}")
                st.write(T[matched]["care"])
                st.write(T[matched]["extra"])
                st.caption(T["nomed"])
            elif any(w in qq for w in ["hi", "hello", "namaskar", "namaste"]):
                st.success(f"🤖 {T['greeting']}")
            else:
                st.info(f"🤖 {T['fallback']}")

# ---------------------------------------------------------------------------
# Tab 3: Hospital finder. Names only. Replace with sourced data (Step 5).
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("🏥 Hospitals in your district")
    hospitals = {
        "Bhubaneswar": ["AIIMS Bhubaneswar", "Capital Hospital", "SUM Ultimate Medicare"],
        "Cuttack": ["SCB Medical College and Hospital", "Cuttack City Hospital"],
        "Puri": ["District Headquarters Hospital, Puri"],
        "Sambalpur": ["VIMSAR, Burla", "District Headquarters Hospital, Sambalpur"],
        "Berhampur": ["MKCG Medical College and Hospital"],
        "Rourkela": ["Ispat General Hospital"],
        "Balasore": ["District Headquarters Hospital, Balasore"],
        "Ganjam": ["MKCG Medical College and Hospital, Berhampur"],
        "Mayurbhanj": ["District Headquarters Hospital, Baripada"],
        "Other": ["Call 104 to find the nearest hospital"],
    }
    for h in hospitals.get(district, hospitals["Other"]):
        st.write(f"✅ {h}")
    st.caption("Hospital list is a starting point. Please confirm details before travelling. Sourced data coming soon.")
    st.success("🚨 Emergency ambulance: **108** | Health helpline: **104**")

# ---------------------------------------------------------------------------
# Tab 4: About (replaces the fake dashboard)
# ---------------------------------------------------------------------------
with tab4:
    st.subheader("About Arogya Mitra")
    st.write(
        "Arogya Mitra is an open-source project built for the Code for a Billion: "
        "Bharat Agentic-AI Hackathon 2026. This pilot focuses on Odisha, with "
        "English, Odia and Hindi support."
    )
    st.write("**Current status:** early prototype. Symptom guidance is rule-based and has not been clinically validated.")
    st.write("**In progress:** conversational AI agent, sourced hospital data, and tested accuracy.")

st.divider()
st.caption(
    "⚠️ Disclaimer: General awareness only. This is not a medical diagnosis and does not replace a doctor. "
    "In an emergency call 108."
)
st.caption("Built for Code for a Billion: Bharat Agentic-AI Hackathon 2026.")
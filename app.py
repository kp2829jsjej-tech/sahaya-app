import os
import streamlit as st
from gtts import gTTS
import io
import time

# ==========================================
# PAGE CONFIGURATION 
# ==========================================
st.set_page_config(
    page_title="Sahaya 3 - Zero Tech Voice Assistant",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Styling for "Zero Tech" Users
st.markdown("""
<style>
    .emergency-card {
        background-color: #ffe6e6;
        border: 2px solid #ff4d4d;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
    }
    .helper-card {
        background-color: #e6f2ff;
        border: 2px solid #66b3ff;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
    }
    .map-btn {
        background-color: #28a745;
        color: white !important;
        padding: 10px 15px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        border-radius: 8px;
        font-weight: bold;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# MULTILINGUAL SUPPORT & BACKEND
# ==========================================
LANGUAGES = {
    "हिन्दी (Hindi)": "hi",
    "தமிழ் (Tamil)": "ta",
    "తెలుగు (Telugu)": "te",
    "বাংলা (Bengali)": "bn",
    "मराठी (Marathi)": "mr",
    "English": "en"
}

def generate_audio(text, lang_code):
    """Converts response text into spoken audio."""
    tts = gTTS(text=text, lang=lang_code, slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

def query_scheme_assistant(query, lang_code):
    """Mock AI engine matching queries to real schemes."""
    query = query.lower()
    if any(k in query for k in ["garbh", "pregnant", "pregnancy", "baby", "paisa"]):
        responses = {
            "hi": "नमस्ते! आप 'मातृ वंदना योजना' के तहत 5,000 रुपये पाने के योग्य हैं।",
            "en": "Hello! You are eligible to receive Rs 5,000 under the 'Matru Vandana Yojana'."
        }
        return responses.get(lang_code, responses["hi"]), "Maternity Scheme Match"
    elif any(k in query for k in ["gas", "cylinder", "chulha"]):
        responses = {
            "hi": "नमस्ते! 'उज्ज्वला योजना' के तहत आपको मुफ्त गैस कनेक्शन मिल सकता है।",
            "en": "Hello! You can get a free gas connection under the 'Ujjwala Yojana'."
        }
        return responses.get(lang_code, responses["hi"]), "Gas Scheme Match"
    else:
        responses = {
            "hi": "नमस्ते! मैं आपकी सहायक हूँ। कृपया अपनी समस्या बोलकर बताएं।",
            "en": "Hello! I am your assistant. Please tell me your problem."
        }
        return responses.get(lang_code, responses["hi"]), "General Help"

# ==========================================
# FRONTEND INTERFACE - SINGLE PAGE DESIGN
# ==========================================
st.markdown("<h1 style='text-align: center;'>🌸 Sahaya (सहायता)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Tap & Speak | No Typing Required</b></p>", unsafe_allow_html=True)

# 1. Top Bar: Language Selection
selected_lang_name = st.selectbox("🌐 भाषा चुनें / Language:", list(LANGUAGES.keys()))
lang_code = LANGUAGES[selected_lang_name]
st.divider()

# ==========================================
# FEATURE 1: SPEAK NOW / VOICE RECORD (Top Priority)
# ==========================================
st.markdown("## 🎙️ 1. Speak Now (बोलें)")
st.info("👇 Tap the microphone below and tell me what you need.")

recorded_audio = st.audio_input("Record voice query")

# Quick demo buttons for the Hackathon Pitch
col1, col2 = st.columns(2)
demo_pregnant = col1.button("🤰 Demo: Pregnancy")
demo_gas = col2.button("🔥 Demo: Gas")

active_prompt = None
if recorded_audio or demo_pregnant:
    active_prompt = "pregnancy"
elif demo_gas:
    active_prompt = "gas cylinder"

if active_prompt:
    with st.spinner("सुन रही हूँ... (Listening...)"):
        time.sleep(1)
        translated_text, logic_match = query_scheme_assistant(active_prompt, lang_code)
        
        st.success("✅ जवाब मिल गया! (Answer Found!)")
        st.markdown(f"> **{translated_text}**")
        
        # Auto-play audio response
        audio_bytes = generate_audio(translated_text, lang_code)
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)

st.divider()

# ==========================================
# FEATURE 2: HELP ME / NEAREST POLICE (Emergency)
# ==========================================
st.markdown("## 🚨 2. Help Me! (आपातकालीन मदद)")
st.write("If you are in danger or need immediate help, tap below.")

st.markdown("""
<div class="emergency-card">
    <h3 style="margin-top:0; color: #cc0000;">🚔 Nearest Police & Helpline</h3>
    <p><b>Women's Helpline:</b> <a href="tel:1091" style="font-size:20px; color:#cc0000;"><b>1091</b></a></p>
    <p><b>Emergency Police:</b> <a href="tel:112" style="font-size:20px; color:#cc0000;"><b>112</b></a></p>
    <a href="https://www.google.com/maps/search/nearest+police+station" target="_blank" class="map-btn" style="background-color: #cc0000;">
        📍 Open Google Maps for Nearest Police
    </a>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# FEATURE 3: LOCAL HELPERS & ANGANWADI (Offline Bridge)
# ==========================================
st.markdown("## 🙋‍♀️ 3. Find Form Helpers (फॉर्म भरने में मदद)")
st.write("Find a trusted local worker (ASHA/Anganwadi) to fill forms for you.")

st.markdown("""
<div class="helper-card">
    <h3 style="margin-top:0; color: #005ce6;">🏥 Local ASHA / Anganwadi</h3>
    <p><b>ASHA Worker (Sunita):</b> <a href="tel:9876543210" style="font-size:18px;">98765-43210</a></p>
    <p><b>Anganwadi Center 4:</b> <a href="tel:9876511223" style="font-size:18px;">98765-11223</a></p>
    <a href="https://www.google.com/maps/search/nearest+anganwadi+center" target="_blank" class="map-btn">
        📍 Open Google Maps for Nearest Anganwadi
    </a>
</div>
""", unsafe_allow_html=True)
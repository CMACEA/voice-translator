import streamlit as st
import speech_recognition as sr
import asyncio
import edge_tts
import os
from deep_translator import GoogleTranslator

# ---------------- CONFIG ----------------
VOICE_LANGS = {
    "English": "en-US-AriaNeural",
    "Spanish": "es-ES-ElviraNeural"
}

AUDIO_DIR = "audio"
AUDIO_FILE = os.path.join(AUDIO_DIR, "voice.wav")
os.makedirs(AUDIO_DIR, exist_ok=True)

# ---------------- TTS ----------------
async def speak(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(AUDIO_FILE)

def speak_sync(text, voice):
    asyncio.run(speak(text, voice))

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="Voice Translator", layout="centered")

st.title("🎤 Voice Translator")
st.caption("Voice translation with premium neural voices")

if os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=150)

spoken_lang = st.selectbox("Spoken language", ["Spanish", "English"])
target_lang = st.selectbox("Translate to", ["English", "Spanish"])

st.divider()
st.write("### 🎧 Voice input")

recognizer = sr.Recognizer()

if st.button("🎙️ Start listening"):
    with sr.Microphone() as source:
        st.info("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        lang_code = "es-ES" if spoken_lang == "Spanish" else "en-US"
        text = recognizer.recognize_google(audio, language=lang_code)

        st.success("You said:")
        st.write(text)

        translated = GoogleTranslator(
            source="es" if spoken_lang == "Spanish" else "en",
            target="en" if target_lang == "English" else "es"
        ).translate(text)

        st.success("Translated text:")
        st.write(translated)

        speak_sync(translated, VOICE_LANGS[target_lang])

        audio_bytes = open(AUDIO_FILE, "rb").read()
        st.audio(audio_bytes, format="audio/wav")

    except Exception:
        st.error("❌ Could not understand the audio")

st.divider()
st.caption("Made by Carlos Macea")




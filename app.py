import streamlit as st
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

# ---------------- UI ----------------
st.set_page_config(page_title="Voice Translator", layout="centered")

st.title("🎤 Voice Translator")
st.caption("Translate text and listen with neural voice")

if os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=150)

spoken_lang = st.selectbox("Spoken language", ["Spanish", "English"])
target_lang = st.selectbox("Translate to", ["English", "Spanish"])

text = st.text_area("✍️ Write the text to translate")

if st.button("🔁 Translate and Speak") and text.strip():
    translated = GoogleTranslator(
        source="es" if spoken_lang == "Spanish" else "en",
        target="en" if target_lang == "English" else "es"
    ).translate(text)

    st.success("Translated text:")
    st.write(translated)

    speak_sync(translated, VOICE_LANGS[target_lang])
    audio_bytes = open(AUDIO_FILE, "rb").read()
    st.audio(audio_bytes, format="audio/wav")

st.divider()
st.caption("Made by Carlos Macea")





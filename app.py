from googletrans import Translator
import streamlit as st
import speech_recognition as sr
import asyncio
import edge_tts
import os

# ---------------- CONFIG ----------------
VOICE_LANGS = {
    "English": "en-US-AriaNeural",
    "Spanish": "es-ES-ElviraNeural"
}

LANG_CODES = {
    "Spanish": "es",
    "English": "en"
}

STT_CODES = {
    "Spanish": "es-ES",
    "English": "en-US"
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

translator = Translator()

input_lang = st.selectbox("🗣 Spoken language", ["Spanish", "English"])
output_lang = st.selectbox("🌍 Translate to", ["English", "Spanish"])

st.divider()
st.write("### 🎧 Voice input")

recognizer = sr.Recognizer()

if st.button("🎙️ Start listening"):
    with sr.Microphone() as source:
        st.info("Listening... Speak a FULL sentence")

        # --- AJUSTES CLAVE PARA NO CORTAR FRASES ---
        recognizer.adjust_for_ambient_noise(source, duration=1)

        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True

        recognizer.pause_threshold = 1.2
        recognizer.non_speaking_duration = 0.5

        audio = recognizer.listen(
            source,
            timeout=10,            # tiempo para empezar a hablar
            phrase_time_limit=25   # tiempo máximo de frase
        )

    try:
        # Speech to text
        text = recognizer.recognize_google(
            audio,
            language=STT_CODES[input_lang]
        )

        st.success("You said:")
        st.write(text)

        # Translation
        translated = translator.translate(
            text,
            src=LANG_CODES[input_lang],
            dest=LANG_CODES[output_lang]
        ).text

        st.success("Translated text:")
        st.write(translated)

        # Text to speech
        speak_sync(translated, VOICE_LANGS[output_lang])

        audio_bytes = open(AUDIO_FILE, "rb").read()
        st.audio(audio_bytes, format="audio/wav")

    except Exception:
        st.error("❌ Could not understand the audio")

st.divider()
st.caption("Made by Carlos Macea")


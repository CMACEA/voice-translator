import streamlit as st
from googletrans import Translator
import edge_tts
import asyncio
import os

# ---------- CONFIG ----------
st.set_page_config(
    page_title="Voice Translator",
    page_icon="🎤",
    layout="centered"
)

# ---------- HEADER ----------
st.title("🎤 Voice Translator")
st.caption("Voice translation with premium neural voices")

if os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=200)

# ---------- TRANSLATOR ----------
translator = Translator()

languages = {
    "Spanish": "es",
    "English": "en",
    "French": "fr",
    "Italian": "it",
    "Portuguese": "pt",
    "German": "de"
}

voices = {
    "en": "en-US-JennyNeural",
    "es": "es-ES-ElviraNeural",
    "fr": "fr-FR-DeniseNeural",
    "it": "it-IT-ElsaNeural",
    "pt": "pt-BR-FranciscaNeural",
    "de": "de-DE-KatjaNeural"
}

# ---------- UI ----------
text = st.text_area("✍️ Text to translate", height=120)

from_lang = st.selectbox("🗣️ Source language", list(languages.keys()), index=0)
to_lang = st.selectbox("🌍 Translate to", list(languages.keys()), index=1)

# ---------- FUNCTION ----------
async def generate_voice(text, lang_code):
    voice = voices.get(lang_code, "en-US-JennyNeural")
    audio_path = "audio/output.mp3"

    tts = edge_tts.Communicate(text=text, voice=voice)
    await tts.save(audio_path)
    return audio_path

# ---------- ACTION ----------
if st.button("▶️ Translate"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        result = translator.translate(
            text,
            src=languages[from_lang],
            dest=languages[to_lang]
        )

        st.success("✅ Translation")
        st.write(result.text)

        with st.spinner("Generating voice..."):
            audio_file = asyncio.run(
                generate_voice(result.text, languages[to_lang])
            )

        st.audio(audio_file)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray;'>Made by Carlos Macea</div>",
    unsafe_allow_html=True
)



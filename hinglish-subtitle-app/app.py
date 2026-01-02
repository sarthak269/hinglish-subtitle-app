import streamlit as st
import openai
import os
import tempfile

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Hinglish Subtitle Generator")

file = st.file_uploader("Upload audio/video", type=["mp3","wav","mp4","m4a"])

if file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        path = tmp.name

    audio = open(path, "rb")

    result = openai.Audio.transcribe(
        file=audio,
        model="whisper-1"
    )

    st.text_area("Transcript", result["text"], height=300)

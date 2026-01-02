import streamlit as st
import os
from openai import OpenAI

st.set_page_config(page_title="Hinglish Subtitle Generator")

st.title("🎬 Hindi → Hinglish Subtitle Generator")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

uploaded_file = st.file_uploader(
    "Upload Hindi audio/video",
    type=["mp3", "wav", "mp4"]
)

if uploaded_file:
    st.success("File uploaded successfully!")

    if st.button("Generate Hinglish Subtitles"):
        with st.spinner("Transcribing..."):
            transcript = client.audio.transcriptions.create(
                file=uploaded_file,
                model="gpt-4o-transcribe"
            )

        st.subheader("📝 Hinglish Output")
        st.text_area("Result", transcript.text, height=300)

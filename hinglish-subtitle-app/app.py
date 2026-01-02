import streamlit as st
import os
import tempfile
from openai import OpenAI

# ---------- Page config ----------
st.set_page_config(
    page_title="Hinglish Subtitle Generator",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Hinglish Subtitle Generator by Techcybe")
st.write("Upload Hindi / Hinglish audio or video and get Hinglish SRT")

# ---------- OpenAI client ----------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- File upload ----------
uploaded_file = st.file_uploader(
    "Upload audio/video",
    type=["mp3", "wav", "mp4", "m4a"]
)

if uploaded_file:
    with st.spinner("Uploading & processing audio..."):
        # save temp file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        # speech to text
        transcript = client.audio.transcriptions.create(
            file=open(tmp_path, "rb"),
            model="gpt-4o-transcribe",
            response_format="srt"
        )

    st.success("✅ Subtitle generated successfully!")
    st.download_button(
        label="⬇️ Download Hinglish SRT",
        data=transcript,
        file_name="hinglish_subtitles.srt",
        mime="text/plain"
    )

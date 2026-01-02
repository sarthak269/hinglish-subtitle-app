import streamlit as st
import whisper
import os

st.set_page_config(page_title="Hinglish Subtitle App by Sarthak", page_icon="🎬")

st.title("🎬 Hinglish Subtitle Generator by Techcybe")
st.write("Upload Hindi / Hinglish video and get Hinglish SRT")

# ---------- Load model once ----------
@st.cache_resource
def load_model():
    return whisper.load_model("medium")

model = load_model()

# ---------- Time formatter ----------
def time_format(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

# ---------- Hinglish polish ----------
REPL = {
    "my name is": "mera naam hai",
    "name is": "naam hai",
    " is ": " hai ",
    "Okay.": "",
    "Okay": "",
    "Hello guys": "hi guys",
    "Hello": "hi"
}

def to_hinglish(text):
    for k, v in REPL.items():
        text = text.replace(k, v)
    return text

# ---------- Upload ----------
video = st.file_uploader("📤 Upload video", type=["mp4", "mkv", "mov"])

if video:
    with open("temp_video.mp4", "wb") as f:
        f.write(video.read())

    st.success("Video uploaded successfully ✅")

    if st.button("🚀 Generate Hinglish SRT"):
        with st.spinner("Processing video..."):
            result = model.transcribe(
                "temp_video.mp4",
                task="transcribe",
                initial_prompt=(
                    "This is a Hinglish YouTube tutorial. "
                    "Write subtitles in Hinglish. "
                    "Do not convert fully to English."
                )
            )

            with open("output_hinglish.srt", "w", encoding="utf-8") as srt:
                for i, seg in enumerate(result["segments"], 1):
                    text = to_hinglish(seg["text"].strip())
                    srt.write(f"{i}\n")
                    srt.write(f"{time_format(seg['start'])} --> {time_format(seg['end'])}\n")
                    srt.write(f"{text}\n\n")

        st.success("🎉 SRT Generated!")

        with open("output_hinglish.srt", "rb") as file:
            st.download_button(
                label="⬇️ Download Hinglish SRT",
                data=file,
                file_name="hinglish_subtitles.srt",
                mime="text/plain"
            )

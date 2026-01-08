import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("processed", False)

# ---------------- CORE IMPORTS ----------------
from core.text_processor import clean_text
from core.translator import translate_to_english
from core.summarizer import summarize_text
from core.image_processor import extract_text_from_image
from core.pdf_processor import extract_text_from_pdf
from core.flashcard_generator import generate_flashcards

#VIDEO ONLY
from core.video_llm import generate_video_summary_and_flashcards

# ---------------- OUTPUT IMPORTS ----------------
from outputs.flowchart import generate_flowchart
from outputs.flashcards import display_flashcards

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Content Summarizer",
    layout="wide"
)

# ===================== SIDEBAR INPUTS =====================
with st.sidebar:
    st.title("Automated Content Summarizer")

    input_type = st.selectbox(
        "Select Input Type",
        ["Text", "PDF", "Image", "Video"]
    )

    raw_text = ""
    video_url = ""

    if input_type == "Text":
        raw_text = st.text_area("Paste your content here", height=200)

    elif input_type == "PDF":
        pdf = st.file_uploader("Upload PDF file", type=["pdf"])
        if pdf:
            raw_text = extract_text_from_pdf(pdf)

    elif input_type == "Image":
        img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
        if img:
            raw_text = extract_text_from_image(img)

    elif input_type == "Video":
        video_url = st.text_input("Enter YouTube video URL")

    generate = st.button("Generate", use_container_width=True)

# ===================== MAIN OUTPUT AREA =====================

#VIDEO PATH (COMPLETELY SEPARATE)
if generate and input_type == "Video" and video_url:
    with st.spinner("Analyzing video context..."):
        summary, cards = generate_video_summary_and_flashcards(video_url)

    st.subheader(" Video Summary")
    st.write(summary)

    st.subheader("Video Flashcards")
    display_flashcards(cards)

# ALL OTHER INPUT TYPES (UNCHANGED)
elif generate and raw_text:
    with st.spinner("Processing content..."):
        cleaned = clean_text(raw_text)
        translated = translate_to_english(cleaned)

        progress = st.progress(0.0)

        def update_progress(value):
            progress.progress(value)

        summary = summarize_text(
            translated,
            progress_callback=update_progress
        )

    st.subheader("Summary")
    for line in summary.split("\n"):
        if line.strip():
            st.markdown(line)

    st.subheader("Concept Flowchart")
    st.graphviz_chart(
        generate_flowchart(translated),
        use_container_width=True
    )

    st.subheader("Q/A Flashcards")
    cards = generate_flashcards(translated)
    display_flashcards(cards)

elif generate:
    st.warning("Please provide valid input content.")

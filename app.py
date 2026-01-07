import streamlit as st

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("processed", False)

# ---------------- IMPORTS ----------------
from core.text_processor import clean_text
from core.translator import translate_to_english
from core.summarizer import summarize_text
from core.video_processor import extract_video_text
from core.image_processor import extract_text_from_image
from core.pdf_processor import extract_text_from_pdf

from outputs.flowchart import generate_flowchart
from outputs.flashcards import generate_flashcards

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Content Summarizer",
    layout="wide"
)

# ===================== SIDEBAR (FIXED INPUT) =====================
with st.sidebar:
    st.title("🌍 Automated Content Summarizer")

    input_type = st.selectbox(
        "Select Input Type",
        ["Text", "PDF", "Image", "Video"]
    )

    raw_text = ""

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
        if video_url:
            raw_text = extract_video_text(video_url)

    generate = st.button("🚀 Generate Summary", use_container_width=True)

# ===================== MAIN OUTPUT AREA =====================
if generate and raw_text:
    st.session_state.processed = True

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

    # -------- SUMMARY --------
    st.subheader("📄 Summary")
    st.markdown("### 📌 Bullet Point Summary")
    for line in summary.split("\n"):
        if line.strip():
            st.markdown(f"- {line.strip()}")

    # -------- FLOWCHART --------
    st.subheader("📊 Concept Flowchart (Generated from Complete Data)")
    st.graphviz_chart(
        generate_flowchart(raw_text),
        use_container_width=True
    )

    # -------- FLASHCARDS --------
    st.subheader("🃏 Flashcards (From Complete Data)")
    cards = generate_flashcards(raw_text)
    for i, card in enumerate(cards, 1):
        st.markdown(f"**Q{i}:** {card['Q']}")
        st.markdown(f"**A{i}:** {card['A']}")

import re
import streamlit as st
from transformers import pipeline


# -------------------------------------------------
# Load Question Generation model (cached, GPU)
# -------------------------------------------------
@st.cache_resource
def load_qg_model():
    return pipeline(
        "text2text-generation",
        model="valhalla/t5-small-qg-prepend",
        device=0  # GPU (use -1 for CPU)
    )


# -------------------------------------------------
# Split text into meaningful sentences
# -------------------------------------------------
def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [
        s.strip()
        for s in sentences
        if len(s.split()) > 7
    ]


# -------------------------------------------------
# Generate flashcards (Question–Answer pairs)
# -------------------------------------------------
def generate_flashcards(raw_text, max_cards=8):
    """
    Generate AI-powered flashcards from cleaned text.

    Returns:
    [
        {
            "question": "...",
            "answer": "..."
        }
    ]
    """
    qg_model = load_qg_model()
    sentences = split_into_sentences(raw_text)

    flashcards = []

    for sentence in sentences:
        prompt = f"generate question: {sentence}"

        try:
            output = qg_model(
                prompt,
                max_new_tokens=48,
                do_sample=False
            )

            question = output[0]["generated_text"]
            question = question.replace("question:", "").strip()

            # Skip bad or very short questions
            if len(question.split()) < 4:
                continue

            flashcards.append({
                "question": question,
                "answer": sentence
            })

            if len(flashcards) >= max_cards:
                break

        except Exception:
            continue

    return flashcards

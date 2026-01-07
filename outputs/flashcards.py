import streamlit as st
import re
from transformers import pipeline

@st.cache_resource
def load_qg_model():
    return pipeline(
        "text2text-generation",
        model="valhalla/t5-small-qg-prepend",
        device=0  # GPU
    )

def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.split()) > 7]

def generate_flashcards(raw_text, max_cards=8):
    """
    Generate AI-powered flashcards from COMPLETE extracted data
    """
    qg = load_qg_model()
    sentences = split_into_sentences(raw_text)

    flashcards = []

    for sentence in sentences:
        prompt = f"generate question: {sentence}"

        try:
            output = qg(
                prompt,
                max_new_tokens=48,
                do_sample=False
            )

            question = output[0]["generated_text"]

            flashcards.append({
                "Q": question,
                "A": sentence
            })

            if len(flashcards) >= max_cards:
                break

        except Exception:
            continue

    return flashcards

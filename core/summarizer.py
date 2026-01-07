import streamlit as st
from transformers import pipeline
import re

@st.cache_resource
def load_summarizer():
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device=0  # GPU
    )

def split_into_chunks(text, max_words=600):
    words = text.split()
    return [
        " ".join(words[i:i + max_words])
        for i in range(0, len(words), max_words)
    ]

def summarize_chunk(summarizer, chunk):
    wc = len(chunk.split())
    max_len = min(140, max(60, wc // 2))
    min_len = max(40, max_len // 2)

    return summarizer(
        chunk,
        max_length=max_len,
        min_length=min_len,
        do_sample=False
    )[0]["summary_text"]

def extract_key_points(text):
    """
    Convert summary paragraph into bullet-ready points
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.split()) > 6]

def summarize_text(text, progress_callback=None, min_points=5, max_points=6):
    summarizer = load_summarizer()
    chunks = split_into_chunks(text)

    all_points = []
    total = len(chunks)

    for i, chunk in enumerate(chunks):
        summary = summarize_chunk(summarizer, chunk)
        points = extract_key_points(summary)
        all_points.extend(points)

        if progress_callback:
            progress_callback((i + 1) / total)

    # 🔒 ENSURE MINIMUM BULLET COUNT
    if len(all_points) < min_points:
        return "\n".join(f"• {p}" for p in all_points)

    # 🎯 SELECT TOP 5–6 POINTS (ORDER PRESERVED)
    final_points = all_points[:max_points]

    return "\n".join(f"• {p}" for p in final_points)

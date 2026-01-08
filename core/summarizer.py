import streamlit as st
from transformers import pipeline
import re


# -------------------------------------------------
# Load summarization model (cached, GPU-enabled)
# -------------------------------------------------
@st.cache_resource
def load_summarizer():
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device=0  # GPU (use -1 for CPU)
    )


# -------------------------------------------------
# Split long text into manageable chunks
# -------------------------------------------------
def split_into_chunks(text, max_words=600):
    words = text.split()
    return [
        " ".join(words[i:i + max_words])
        for i in range(0, len(words), max_words)
    ]


# -------------------------------------------------
# Summarize a single chunk safely
# -------------------------------------------------
def summarize_chunk(summarizer, chunk):
    wc = len(chunk.split())

    max_len = min(160, max(70, wc // 2))
    min_len = max(50, max_len // 2)

    return summarizer(
        chunk,
        max_length=max_len,
        min_length=min_len,
        do_sample=False
    )[0]["summary_text"]


# -------------------------------------------------
# Universal, domain-agnostic sentence categorization
# -------------------------------------------------
def extract_key_points(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    sections = {
        "highlights": [],
        "ideas": [],
        "details": [],
        "practical": [],
        "takeaway": []
    }

    for s in sentences:
        s = s.strip()
        s_lower = s.lower()

        if len(s.split()) < 6:
            continue

        if any(k in s_lower for k in ["overview", "introduction", "explains", "discusses"]):
            sections["highlights"].append(s)

        elif any(k in s_lower for k in ["idea", "concept", "principle", "approach"]):
            sections["ideas"].append(s)

        elif any(k in s_lower for k in ["includes", "covers", "details", "features"]):
            sections["details"].append(s)

        elif any(k in s_lower for k in ["example", "application", "use case", "practice"]):
            sections["practical"].append(s)

        else:
            sections["takeaway"].append(s)

    return sections


# -------------------------------------------------
# MAIN FUNCTION – Universal Structured Summary
# -------------------------------------------------
def summarize_text(text, progress_callback=None):
    summarizer = load_summarizer()
    chunks = split_into_chunks(text)

    final_sections = {
        "highlights": [],
        "ideas": [],
        "details": [],
        "practical": [],
        "takeaway": []
    }

    total = len(chunks)

    for i, chunk in enumerate(chunks):
        summary = summarize_chunk(summarizer, chunk)
        extracted = extract_key_points(summary)

        for key in final_sections:
            final_sections[key].extend(extracted.get(key, []))

        if progress_callback:
            progress_callback((i + 1) / total)

    # -------------------------------------------------
    # 🔥 SMART FALLBACK LOGIC (CRITICAL)
    # -------------------------------------------------
    all_sentences = []
    for v in final_sections.values():
        all_sentences.extend(v)

    all_sentences = list(dict.fromkeys(all_sentences))  # remove duplicates

    # If only takeaway is populated, redistribute
    non_empty = [k for k, v in final_sections.items() if v]

    if len(non_empty) <= 1 and all_sentences:
        final_sections["highlights"] = all_sentences[:2]
        final_sections["ideas"] = all_sentences[2:4]
        final_sections["details"] = all_sentences[4:6]
        final_sections["practical"] = all_sentences[6:7]
        final_sections["takeaway"] = all_sentences[-1:]

    # -------------------------------------------------
    # Output formatting
    # -------------------------------------------------
    output = []

    def add_section(title, items, limit):
        if items:
            output.append(title)
            output.extend(f"• {s}" for s in items[:limit])
            output.append("")

    add_section("🔹 Key Highlights", final_sections["highlights"], 2)
    add_section("🔹 Main Ideas", final_sections["ideas"], 2)
    add_section("🔹 Important Details", final_sections["details"], 2)
    add_section("🔹 Practical / Real-World Aspects", final_sections["practical"], 1)

    if final_sections["takeaway"]:
        output.append("🔹 Purpose / Takeaway")
        output.append(final_sections["takeaway"][0])

    return "\n".join(output)
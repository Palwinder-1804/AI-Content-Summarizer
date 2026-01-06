import streamlit as st
from translator import detect_language, translate_to_english, translate_from_english
from summarizer import generate_summary

st.set_page_config(page_title="AI Multilingual Summarizer", layout="wide")

st.title("🌍 AI-Based Multilingual Content Summarizer")
st.write("Enter text in **any language** to get a concise summary.")

input_text = st.text_area("📥 Enter your content:", height=250)

summary_length = st.slider("Summary Length", 50, 200, 120)

if st.button("Generate Summary"):
    if input_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Processing..."):
            lang = detect_language(input_text)
            english_text = translate_to_english(input_text, lang)
            
            summary_en = generate_summary(
                english_text,
                max_len=summary_length
            )
            
            final_summary = translate_from_english(summary_en, lang)

        st.success("Summary Generated!")
        st.subheader("📄 Summary")
        st.write(final_summary)

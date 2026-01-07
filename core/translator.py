from langdetect import detect
from transformers import pipeline

translator = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-mul-en",
    device=0  # use -1 if no GPU
)

def translate_to_english(text):
    try:
        lang = detect(text)
        if lang != "en":
            return translator(text)[0]["translation_text"]
    except:
        pass
    return text
from langdetect import detect
from deep_translator import GoogleTranslator

def detect_language(text):
    return detect(text)

def translate_to_english(text, src_lang):
    if src_lang != "en":
        return GoogleTranslator(source=src_lang, target="en").translate(text)
    return text

def translate_from_english(text, target_lang):
    if target_lang != "en":
        return GoogleTranslator(source="en", target=target_lang).translate(text)
    return text

from transformers import pipeline
from typing import Literal
from langdetect import detect
import re

# define Hugging models
en_to_es = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")
es_to_en = pipeline("translation_es_to_en", model="Helsinki-NLP/opus-mt-es-en")
en_to_fr = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
fr_to_en = pipeline("translation_fr_to_en", model="Helsinki-NLP/opus-mt-fr-en")
es_to_fr = pipeline("translation_es_to_fr", model="Helsinki-NLP/opus-mt-es-fr")
fr_to_es = pipeline("translation_fr_to_es", model="Helsinki-NLP/opus-mt-fr-es")

def translate_text(text: str, target_lang: Literal["english", "spanish", "french"]) -> str:
    translated_sentences = []

    lang_map = {
       "english": "en",
       "spanish": "es",
       "french": "fr"
    }

    target_code = lang_map.get(target_lang.lower())
    if not target_code:
        raise ValueError(f"Unsupported target language {target_lang}")
    
    models = {
        ("en", "es"): en_to_es,
        ("es", "en"): es_to_en,
        ("en", "fr"): en_to_fr,
        ("fr", "en"): fr_to_en,
        ("es", "fr"): es_to_fr,
        ("fr", "es"): fr_to_es
    }
    
    # we run this try statement just in case we insert a bad input that wouldn't allow detect to classify the language being used 
    try:
        source_lang = detect(text)
    except:
        source_lang = None # sets source_lang to None of a bad input is used

    fallback_sources = ["en", "es", "fr"]

    # this conditional logic here allows us to assign source_lang the correct language being used if we weren't able to set one with the try case
    if not source_lang or source_lang == target_code or (source_lang, target_code) not in models:
        for fallback in fallback_sources:
            if fallback == target_code:
                continue
            if (fallback, target_code) in models:
                source_lang = fallback
                break
    
    model = models.get((source_lang, target_code))
    
    if not model:
        raise ValueError(f"Unsupported language pair {source_lang} to {target_code}")
   
    split_chunks = re.split(r'(?<=[.!?])\s+', text)

    for chunk in split_chunks:
        if chunk.strip():
            result = model(chunk)
            translated_sentences.append(result[0]["translation_text"])
        
    return " ".join(translated_sentences)

print(translate_text("Hello", "spanish"))
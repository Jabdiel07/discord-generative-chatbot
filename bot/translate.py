from transformers import pipeline
from typing import Literal
from langdetect import detect
import re

# load the predefined translation pipelines
# the first argument tells the Hugging Face model what kind of task I want to perform, there's a list of predetermined tasks you can find online
en_to_es = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")
es_to_en = pipeline("translation_es_to_en", model="Helsinki-NLP/opus-mt-es-en")
en_to_fr = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
fr_to_en = pipeline("translation_fr_to_en", model="Helsinki-NLP/opus-mt-fr-en")
es_to_fr = pipeline("translation_es_to_fr", model="Helsinki-NLP/opus-mt-es-fr")
fr_to_es = pipeline("translation_fr_to_es", model="Helsinki-NLP/opus-mt-fr-es")

'''
def chunk_text(text: str, max_chunks: int = 400) -> list[str]:
    split_chunks = re.split(r'(?<=[.!?])\s*', text.split())
    #print(split_chunks)

    chunks = [] # will hold the final grouped texts
    current_chunk = "" # holds the current chunk

    for chunk in split_chunks:
        if len(current_chunk) + len(chunk) <= max_chunks: # if the length of the current chunk plus the chunk we're on is less or equal to max_chunk
            current_chunk += chunk + " " # we want to add the chunk we're iterating over into current chunk
            #print(current_chunk)
        else:
            chunks.append(current_chunk.strip()) # if the previous conditional is false, we want to append whatever we have in current chunk into the chunks list
            current_chunk = chunk + " " # and then we reset the current chunk by assigning it just the chunk we're currently iterating over
    
    if current_chunk: # if there are still things inside of current chunk that we didn't add the the chunks list, then we add it in this conditional
        chunks.append(current_chunk.strip()) # strip removes the leading or trailing whitespace in the string. So something like "Hello there. How are you? " would be "Hello there. How are you?" 
    
    return chunks
'''

def translate_text(text: str, target_lang: Literal["english", "spanish", "french"]) -> str:  # literal tells the type checker tools that target_language value can only be 'en' or 'es'
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
    '''
    if target_lang == "spanish":
        model = en_to_es
    elif target_lang == "english":
        model = es_to_en
    else:
        raise ValueError("Unsupported target language. Use 'en' for English or 'es' for Spanish. ") # raise ValueError shows a user an error message if none of the previous conditions are true and terminates the whole execution of the program
    '''
    split_chunks = re.split(r'(?<=[.!?])\s+', text)

    for chunk in split_chunks:
        if chunk.strip(): # split will remove any leading and trailing spaces and makes sure that empty strings don't get translated (this would be a waste of resources and can output weird whitespaces in the results)
            result = model(chunk)
            translated_sentences.append(result[0]["translation_text"]) # here we grab the first element of the translated list, which is a dictionary and then we grab the value of the key "translation_text"
        
    return " ".join(translated_sentences)

print(translate_text("Hello", "spanish"))

#print(chunk_text("Hello there. How are you? That's great! See you"))
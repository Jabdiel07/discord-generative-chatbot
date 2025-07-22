from transformers import pipeline
from typing import Literal
import re

# load the predefined translation pipelines
# the first argument tells the Hugging Face model what kind of task I want to perform, there's a list of predetermined tasks you can find online
en_to_es = pipeline("translation_en_to_es", model="Helsinki-NLP/opus-mt-en-es")
es_to_en = pipeline("translation_es_to_en", model="Helsinki-NLP/opus-mt-es-en")
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

def translate_text(text: str, target_lang: Literal["english", "spanish"]) -> str:  # literal tells the type checker tools that target_language value can only be 'en' or 'es'
    if target_lang == "spanish":
        translated = en_to_es(text)
    elif target_lang == "english":
        translated = es_to_en(text)
    else:
        raise ValueError("Unsupported target language. Use 'en' for English or 'es' for Spanish. ") # raise ValueError shows a user an error message if none of the previous conditions are true and terminates the whole execution of the program

    return translated[0]["translation_text"] # here we grab the first element of the translated list, which is a dictionary and then we grab the value of the key "translation_text"

print(translate_text("Hola qué hay? Cómo estás?", "english"))

#print(chunk_text("Hello there. How are you? That's great! See you"))
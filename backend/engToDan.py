
from typing import Any
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

 
class EngToDanTranslator():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-da")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-da")

    def __call__(self, english_text) :
        input_ids = self.tokenizer.encode(english_text, return_tensors="pt")
        translated_ids = self.model.generate(input_ids)
        translated_text = self.tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        return translated_text
        



# input_ids = tokenizer.encode(english_text, return_tensors="pt")

# translated_ids = model.generate(input_ids)

# translated_text = tokenizer.decode(translated_ids[0], skip_special_tokens=True)

 

# print("English:", english_text)

# print("Translated Danish:", translated_text)
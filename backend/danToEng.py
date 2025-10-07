
from typing import Any
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class DanToEngTranslator():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-da-en")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-da-en")

    def __call__(self, danish_text) :
        input_ids = self.tokenizer.encode(danish_text, return_tensors="pt")
        translated_ids = self.model.generate(input_ids)
        translated_text = self.tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        return translated_text
from typing import Any
from llama_cpp import Llama

text="Q: Name the planets in the solar system? A: "

class Llama2 :
    def __init__(self) :
        self.llm = Llama(model_path="./models/llama-2-7b-chat.ggmlv3.q4_0.bin", n_ctx=2000)

    def __call__(self,prompt):
        output = self.llm( prompt=prompt,max_tokens=4000, echo=True)
        return output

    
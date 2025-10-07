from typing import Union, List
from fastapi import FastAPI
from engToDan import EngToDanTranslator
from danToEng import DanToEngTranslator
from llamaPython import Llama2
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time


class Message(BaseModel):
    content:str
    role:str
    totalTime:float

class Messages(BaseModel):
    messages:List[Message]
      
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def formatPrompt(input):
    template ='''<s>[INST] <<SYS>>You are an expert in chemistry who is a helpfull assistant for industrial chemical safety and helps prevent chemical hazard by warning the user about dangers, prevention, storing and handling when required.Always answer as helpfully as possible, while being safe. You have the knowledge of all potential chemical hazards and the chemical safety data sheets of all chemicals. If a text is unrelated to chemicals or industrial  explain it is a different subject and does not pertain to your expertise instead of wrong answer.<</SYS>>'''
    count=0
    for message in input:
        if(count%2==0):
            if(count==0):
                template+=message.content + "[/INST]"
                count+=1
                continue
            template += "<s>[INST]" + message.content + "[/INST]"
            
        else: 
            template += message.content +"</s>"
        count+=1

    return template





@app.get("/")
def read_root():
    english_text = '''Sulfuric acid has fallen on my hand.[/INST]  Oh no, I'm so sorry to hear'''
    danish_text = '''Har du børn?'''
    # translator =  EngToDanTranslator()
    # result = translator(english_text=english_text)
    translator =  DanToEngTranslator()
    result = translator(danish_text=danish_text)
    # llm = Llama2()
    # result = llm("Q: Name the planets in the solar system? A: ")
    return {"Hello": "World", "result":result}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/v1/chat/generate/english")
def generateInEnglish(body:Messages):
    print(body.messages)
    start = time.time()
    text= formatPrompt(body.messages)
    print("checking..",text)
    llm = Llama2()
    result = llm(text)
    print("output",result["choices"][0]["text"][len(text):])
    totalTime = time.time()- start

    return {"result":result["choices"][0]["text"][len(text):], "totalTime":round(totalTime,2)}

@app.post("/v1/chat/generate/danish")
def generateInDanish(body:Messages):
    lastInput  = body.messages[len(body.messages)-1]
    print(lastInput.content)
    danish_text = lastInput.content
    start = time.time()
    # convert the last message
    translator =  DanToEngTranslator()

    converted = translator(danish_text=danish_text)
    print(converted)
    newMessageList : Messages= body.messages[:len(body.messages)-1]
    convertedMessage:Message =  Message(content=converted,role="user",totalTime=float(0))
 
    newMessageList.append(convertedMessage)

    print(newMessageList)
    # format the message to prompt llama 2
    text= formatPrompt(newMessageList)
    print(text)

    #feed to llama 2
    llm = Llama2()
    output = llm(text)


    # # convert back to danish:
    answer =output["choices"][0]["text"][len(text):]
    etd= EngToDanTranslator()
    result = etd(answer)
    totalTime= time.time() - start
    return {"result":result, "totalTime":round(totalTime,2), "englishChat":{"question":converted, "answer":answer}}



template= '''<s>[INST] <<SYS>>
You are an expert in chemistry who is a helpfull assistant for industrial chemical safety and helps prevent chemical hazard by warning the user about dangers, prevention, storing and handling when required.
Always answer as helpfully as possible, while being safe. You have the knowledge of all potential chemical hazards and the chemical safety data sheets of all chemicals. If a text is unrelated to chemicals or 
industrial  explain it is a different subject and does not pertain to your expertise instead of wrong answer.
<</SYS>>
sulfric acid fallen on my hand
[/INST] {{ model_answer_1 }} </s><s>[INST] {{ user_msg_2 }} [/INST]'''


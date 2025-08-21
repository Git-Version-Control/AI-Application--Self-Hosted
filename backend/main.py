from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.document import router as document_router
from backend.chat import router as chat_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(document_router)
app.include_router(chat_router)

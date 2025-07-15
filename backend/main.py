from fastapi import FastAPI, Request
from pydantic import BaseModel
from intent_engine import extract_intent
from mcp_layer import search_files, open_file
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from file_chatbot import ask_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ใน production ควรระบุ domain ให้ปลอดภัย
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class FileResult(BaseModel):
    name: str
    path: str

class FileQuestionRequest(BaseModel):
    path: str
    question: str

@app.get("/")
async def root():
    return {"message": "Root Page"}

@app.post("/chat", response_model=List[FileResult])
def chat_endpoint(req: ChatRequest):
    message = req.message
    print(f"[USER MESSAGE] {message}")
    intent_data = extract_intent(message)
    print(f"[INTENT] {intent_data}")
    print("-----------------------")

    if intent_data["intent"] == "search_file":
        results = search_files(intent_data)
        for r in results:
            print(f"[FILE NAME] {r['name']}")
            print(f"[FILE PATH FOUND] {r['path']}")
            print("-----------------------")
        return results

    elif intent_data["intent"] == "open_file":
        results = search_files(intent_data)
        print(f"[OPEN FILE] {results}")
        if results:
            open_file(results[0]["path"])
            print("-----------------------")
        return results

    return []

@app.post("/ask-file")
def ask_about_file(req: FileQuestionRequest):
    answer = ask_question(req.path, req.question)
    print(f"[INFORMATION FORM] {req.path}")
    print(f"[BOT ANSWER] {answer}")
    return {"answer": answer}
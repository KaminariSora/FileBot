from fastapi import FastAPI, Request
from pydantic import BaseModel
from intent_engine import extract_intent
from mcp_layer import search_files, open_file
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

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

class PathRequest(BaseModel):
    path: str

class FileResult(BaseModel):
    name: str
    path: str

class FileOpenRequest(BaseModel):
    filepath: str

class FileQuestionRequest(BaseModel):
    path: str
    question: str

@app.get("/")
async def root():
    return {"message": "Root Page"}

global_search_path = ""

@app.post("/search-path")
def path_endpoint(req: PathRequest):
    global global_search_path
    path = Path(req.path)
    if path.exists() and path.is_dir():
        global_search_path = str(path)
        return {"exists": True, "path": str(path)}
    else:
        return {"exists": False, "path": str(path)}
    
@app.post("/intent-text", response_model=List[FileResult])
def chat_endpoint(req: ChatRequest):
    message = req.message
    print(f"[USER MESSAGE] {message}")
    intent_data = extract_intent(message)
    print(f"[INTENT] {intent_data}")
    print("-----------------------")

    if intent_data["intent"] == "search_file":
        print("Path",global_search_path)
        results = search_files(intent_data, global_search_path)
        for r in results:
            print(f"[FILE NAME] {r['name']}")
            print(f"[FILE PATH FOUND] {r['path']}")
            print("-----------------------")
        return results

    elif intent_data["intent"] == "open_file":
        results = search_files(intent_data, global_search_path)
        print(f"[OPEN FILE] {results}")
        if results:
            open_file(results[0]["path"])
            print("-----------------------")
        return results

    return []

@app.post("/open-file")
def open_file(req: FileOpenRequest):
    filepath = req.filepath
    try:
        file_path = Path(filepath)
        if not file_path.exists():
            raise FileNotFoundError(f"ไม่พบไฟล์: {filepath}")
        
        # Windows
        if os.name == 'nt':
            os.startfile(filepath)
        # macOS
        elif os.name == 'posix' and os.uname().sysname == 'Darwin':
            os.system(f'open "{filepath}"')
        # Linux
        else:
            os.system(f'xdg-open "{filepath}"')
            
        return {"success": True, "message": f"เปิดไฟล์ {file_path.name} เรียบร้อยแล้ว"}
    except Exception as e:
        return {"success": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}

@app.post("/ask-file")
def ask_about_file(req: FileQuestionRequest):
    answer = ask_question(req.path, req.question)
    print(f"[INFORMATION FORM] {req.path}")
    print(f"[BOT ANSWER] {answer}")
    return {"answer": answer}
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service/service_account.json"

class IntentSchema(BaseModel):
    intent: str = Field(description="ประเภท intent เช่น search_file, open_file")
    filename: str | None = Field(default=None, description="ชื่อไฟล์หรือตัวค้นหาในชื่อไฟล์")
    type: str | None = Field(default=None, description="นามสกุลไฟล์ เช่น .pdf, .pptx")
    modified_within_days: int | None = Field(default=None, description="จำนวนวันที่ไฟล์ถูกแก้ไขภายใน")

prompt = ChatPromptTemplate.from_messages([
    ("system", "คุณคือผู้ช่วยที่วิเคราะห์ข้อความผู้ใช้และตอบกลับเป็น JSON ที่มี key: intent, filename, type, modified_within_days"),
    ("human", "ข้อความ: {message}\nโปรดตอบกลับ JSON เท่านั้น เช่น:\n"
              '{{ "intent": "search_file", "filename": "report", "type": ".pdf", "modified_within_days": 3 }}')
])

llm = init_chat_model(
    "gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.8
)

parser = JsonOutputParser(pydantic_schema=IntentSchema)

chain = prompt | llm | parser

def extract_intent(message: str):
    try:
        result = chain.invoke({"message": message})
        return result.dict()
    except Exception as e:
        print(f"[INTENT ERROR] {e}")
        return {
            "intent": "search_file",
            "filename": None,
            "type": None,
            "modified_within_days": None
        }

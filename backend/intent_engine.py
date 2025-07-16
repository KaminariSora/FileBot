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
    ("system", """คุณคือผู้ช่วยที่วิเคราะห์ข้อความผู้ใช้และตอบกลับเป็น JSON 
    
        ประเภท intent ที่เป็นไปได้:
        - search_file: เมื่อผู้ใช้ต้องการค้นหาไฟล์
        - open_file: เมื่อผู้ใช้ต้องการเปิดไฟล์

        คำที่สื่อถึงการค้นหา: ค้นหา, หา, ต้องการดู, มีไฟล์อะไรบ้าง
        คำที่สื่อถึงการเปิด: เปิด, เปิดไฟล์, แสดงไฟล์

        หากข้อความไม่ชัดเจนให้เลือก search_file

        ตัวอย่าง:
        - "หาไฟล์ pdf" -> search_file
        - "เปิดไฟล์ชื่อ report.pdf" -> open_file
        - "ค้นหาไฟล์ excel ที่ใช้เมื่อ 2 วันก่อน" -> search_file
        - "เปิดไฟล์นี้" -> open_file
        """),
    ("human", "ข้อความ: {message}\nโปรดตอบกลับ JSON เท่านั้น เช่น:\n"
              '{{ "intent": "search_file", "filename": "report", "type": ".pdf", "modified_within_days": 3 }}\n'
              'หรือ {{ "intent": "open_file", "filename": "report.pdf", "type": null, "modified_within_days": null }}')
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
        print(f"[DEBUG][Class {type(result)}] Result: {result}")
        
        if isinstance(result, dict):
            return result
        elif hasattr(result, 'dict'):
            return result.dict()
        else:
            return dict(result)
    except Exception as e:
        print(f"[INTENT ERROR] {e}")
        return {
            "intent": "search_file",
            "filename": None,
            "type": None,
            "modified_within_days": None
        }

import os
from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader, UnstructuredExcelLoader,
    UnstructuredImageLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service/service_account.json"

def load_file(file_path: str):
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        return PyPDFLoader(file_path).load()
    elif ext in [".txt"]:
        return TextLoader(file_path).load()
    elif ext in [".doc", ".docx"]:
        return UnstructuredWordDocumentLoader(file_path).load()
    elif ext in [".md"]:
        return UnstructuredMarkdownLoader(file_path).load()
    elif ext in [".xls", ".xlsx"]:
        return UnstructuredExcelLoader(file_path).load()
    elif ext in [".png", ".jpg", ".jpeg"]:
        return UnstructuredImageLoader(file_path).load()
    else:
        raise ValueError(f"ไม่รองรับไฟล์ประเภทนี้: {ext}")

def ask_question(file_path: str, question: str):
    documents = load_file(file_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embedding_model = VertexAIEmbeddings(
        model_name="gemini-embedding-001",
        location="us-central1"
    )   

    vector_store = InMemoryVectorStore(embedding=embedding_model)
    for i, doc_item in enumerate(chunks):
        doc = doc_item if isinstance(doc_item, Document) else Document(page_content=str(doc_item))
        vector_store.add_documents([doc])

    retrievers = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "คุณคือผู้ช่วยที่ตอบคำถามจากเนื้อหาในไฟล์"),
        ("human", "คำถาม: {question}, ข้อมูลที่เกี่ยวข้อง: {context}")
    ])

    llm = init_chat_model(
        "gemini-2.0-flash",
        model_provider="google_genai",
        temperature=0.8
    )

    docs = retrievers.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    qa_chain = (
        RunnableLambda(lambda x: {"context": context, "question": x})
        | prompt
        | llm
        | StrOutputParser()
    )

    return qa_chain.invoke(question)

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service/service_account.json"

def ask_question(file_path: str, question: str):
    loader = PyPDFLoader(file_path=file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embedding_model = VertexAIEmbeddings(
        model_name="gemini-embedding-001",
        location="us-central1"
    )   

    vector_store = InMemoryVectorStore(embedding=embedding_model)
    print("Adding documents one by one...")
    for i, doc_item in enumerate(chunks):
        try:
            if isinstance(doc_item, Document):
                doc = doc_item
                print(f"Document {i+1} is already a Document object")
            elif isinstance(doc_item, str):
                doc = Document(page_content=doc_item)
                print(f"Created Document object from string: {doc_item}")
            else:
                doc = Document(page_content=str(doc_item))
                print(f"Converted to string and created Document: {str(doc_item)}")

            vector_store.add_documents([doc])
            print(f"✓ Successfully added document {i+1}")

        except Exception as e:
            print(f"✗ Error adding document {i+1}: {str(e)}")

    print(f"\nCompleted adding documents to vector store!")

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

    # 7. รวมเป็น chain แล้วถาม
    qa_chain = (
    RunnableLambda(lambda x: {"context": context, "question": x})
    | prompt
    | llm
    | StrOutputParser()
)

    return qa_chain.invoke(question)
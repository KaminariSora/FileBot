import os
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./backend/service/service_account.json"

loader = TextLoader('####',encoding='utf-8')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=0
)
chunks = text_splitter.split_documents(documents)

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

retrievers = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}  # Retrieve top 3 most relevant chunks
)

prompt = ChatPromptTemplate.from_messages([
    ("system","ใช้ข้อมูลจากเอกสารในการตอบคำถามให้สั้นกระชับด้วยความสุภาพเป็นกันเอง"),
    ("human","คำถาม: {question} , ข้อมูลที่เกี่ยวข้อง: {context}")
])

# model
llm = init_chat_model(
    "gemini-2.0-flash",
    model_provider="google_genai",
    temperature=0.8
)

# 
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# ใช้วิธีอื่นแก้เพื่อป้องกันปัญหา RunnablePassthrough
def get_context_and_question(query):
    # Get relevant documents
    docs = retrievers.invoke(query)
    context = format_docs(docs)
    return {"context": context, "question": query}

rag_chain = (
    get_context_and_question
    | prompt
    | llm
    | StrOutputParser()
)

# OR try this simpler approach using lambda:
# rag_chain = (
#     (lambda x: {"context": format_docs(retrievers.invoke(x)), "question": x})
#     | prompt
#     | llm
#     | StrOutputParser()
# )

while True:
    user_input = input("Enter your question: ")

    if user_input.lower() in ["quit","q","exit"]:
        print("exited.")
    else:
        result = rag_chain.invoke(user_input)
        print(result)
import os
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./backend/service/service_account.json"

loader = TextLoader('data.txt',encoding='utf-8')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0
)
chunks = text_splitter.split_documents(documents)
print(chunks)

# documents = [
#     "ชื่อบริษัท : KamiSora",
#     "ข้อมูลธุรกิจ : จัดจำหน่ายของเล่นและหนังสือการ์ตูน",
#     "ผู้ก่อตั้ง : โซระ",
#     "ปีที่ก่อตั้ง : 2568",
# ]

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

query = "โซระ"
print(f"\nSearching for: '{query}'")

results = vector_store.similarity_search(query, k=2)
print("\nTop 2 results:")
for i, result in enumerate(results, 1):
    print(f"{i}. {result.page_content}")

retrievers = vector_store.as_retriever()
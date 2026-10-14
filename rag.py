import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DOCS_DIR = "./documents"
DB_DIR = "./vector_db"

# Auto-create documents folder if missing
if not os.path.exists(DOCS_DIR):
    os.makedirs(DOCS_DIR)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    embedding_function=embeddings,
    collection_name="finance_documents",
    persist_directory=DB_DIR,
)

def load_and_ingest():
    all_chunks = []
    
    if not os.path.exists(DOCS_DIR) or len(os.listdir(DOCS_DIR)) == 0:
        return "No PDF files found in ./documents directory."

    for file_name in os.listdir(DOCS_DIR):
        if not file_name.lower().endswith(".pdf"):
            continue

        path = os.path.join(DOCS_DIR, file_name)
        loader = PyPDFLoader(path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=250,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        chunks = splitter.split_documents(docs)

        for chunk in chunks:
            chunk.metadata["source_file"] = file_name
            chunk.metadata["page"] = chunk.metadata.get("page", "unknown")

        all_chunks.extend(chunks)

    if all_chunks:
        vector_store.add_documents(all_chunks)
        return f"Successfully ingested {len(all_chunks)} chunks from PDFs."
    
    return "No chunk content generated."

def retrieve_documents(query: str, k: int = 4):
    return vector_store.similarity_search(query, k=k)

if __name__ == "__main__":
    print("RAG Module Initialized Successfully!")
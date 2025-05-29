import os
import json
import shutil
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# .env-Datei laden
load_dotenv()

# Dateipfade
DATA_PATH = "structured_data.json"
CHROMA_DIR = "chroma_langchain_db"

def load_structured_data(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Document(page_content=item["content"], metadata=item) for item in data]

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)

def embed_and_store(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    # Alte Datenbank löschen, falls vorhanden
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    # Neue Datenbank erstellen
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    return db

def main():
    print("🔄 Daten werden geladen...")
    documents = load_structured_data(DATA_PATH)
    print(f"📄 {len(documents)} Dokumente gefunden.")

    print("✂️ Chunking wird gestartet...")
    chunks = chunk_documents(documents)
    print(f"✅ {len(chunks)} Chunks wurden erstellt.")

    print("📦 Embedding und Speicherung in Chroma...")
    embed_and_store(chunks)
    print(f"✅ Alle Daten wurden in '{CHROMA_DIR}' gespeichert.")

if __name__ == "__main__":
    main()

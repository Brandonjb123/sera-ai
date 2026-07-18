# ============================================================
# SERA AI — RAG Engine (ChromaDB + TF-IDF + LangChain)
# ============================================================
import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import chromadb
from chromadb.config import Settings
from embeddings import encode
import asyncio


# Inisialisasi ChromaDB — folder di /app/data (persisten via Railway Volume)
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
os.makedirs(CHROMA_PATH, exist_ok=True)
chroma_client = chromadb.Client(Settings(persist_directory=CHROMA_PATH))
collection = chroma_client.get_or_create_collection(name="documents")

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "rag_data.pkl")

# Muat data yang sudah ada (jika ada)
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as f:
        data = pickle.load(f)
        documents = data.get("documents", [])
        doc_names = data.get("doc_names", [])
        vectorizer = data.get("vectorizer", None)
        doc_vectors = data.get("doc_vectors", None)
else:
    documents = []
    doc_names = []
    vectorizer = None
    doc_vectors = None

def save_data():
    """Simpan state ke file pickle."""
    with open(DATA_FILE, "wb") as f:
        pickle.dump({
            "documents": documents,
            "doc_names": doc_names,
            "vectorizer": vectorizer,
            "doc_vectors": doc_vectors
        }, f)

def extract_text_from_pdf(file_path):
    """Ekstrak teks dari file PDF."""
    reader = PyPDF2.PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

async def add_document(file_path):
    """Tambahkan dokumen ke ChromaDB (dan update TF-IDF untuk fallback)."""
    global documents, doc_names, vectorizer, doc_vectors

    file_name = os.path.basename(file_path)

    # Ekstrak teks
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

    if not text.strip():
        return 0, "Dokumen kosong"

    # Update TF-IDF (untuk fallback, tidak dipakai di pencarian utama)
    documents.append(text)
    doc_names.append(file_name)
    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(documents)
    save_data()

    # Generate embedding untuk ChromaDB
    embedding = await asyncio.to_thread(encode, text)

    # Simpan ke ChromaDB
    doc_id = str(len(doc_names))
    collection.add(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"source": file_name}]
    )

    return len(doc_names), file_name

async def search(query, n_results=3):
    """Cari dokumen paling relevan menggunakan embedding ChromaDB."""
    query_embedding = await asyncio.to_thread(encode, query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    formatted_results = []
    for i in range(len(results['documents'][0])):
        formatted_results.append({
            "document": results['documents'][0][i],
            "source": results['metadatas'][0][i]['source'],
            "score": 1.0
        })
    
    return formatted_results

def clear_documents():
    """Hapus semua dokumen dari ChromaDB dan TF-IDF."""
    global documents, doc_names, vectorizer, doc_vectors
    documents = []
    doc_names = []
    vectorizer = None
    doc_vectors = None
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    
    # Hapus semua dari ChromaDB
    collection.delete(ids=collection.get()['ids'])

def get_document_count():
    """Kembalikan jumlah dokumen yang tersimpan."""
    return len(documents)
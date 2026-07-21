# ============================================================
# SERA AI — Backend FastAPI (Fase 0 + Fase 1 + Fase 2 + Fase 3 + BYOK)
# ============================================================
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import os
import shutil
import uvicorn

# ============================================================
# LOAD ENVIRONMENT & SETUP CLIENT
# ============================================================
load_dotenv()

groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

ADMIN_USER = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "sera123")

# ============================================================
# INISIALISASI APLIKASI
# ============================================================
app = FastAPI(
    title="Sera AI API",
    description="Backend untuk chatbot customer service RAG",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sera-ai-two.vercel.app",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# ============================================================
# AUTHENTICATION
# ============================================================
def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verifikasi token admin sederhana."""
    token = credentials.credentials
    import base64
    try:
        decoded = base64.b64decode(token).decode("utf-8")
        username, password = decoded.split(":", 1)
        if username == ADMIN_USER and password == ADMIN_PASS:
            return username
    except:
        pass
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Autentikasi gagal. Gunakan token yang valid."
    )

@app.post("/admin/login")
async def admin_login(username: str, password: str):
    """Login admin dan dapatkan token."""
    if username == ADMIN_USER and password == ADMIN_PASS:
        import base64
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        return {"token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Username atau password salah")

# ============================================================
# IMPORT RAG ENGINE & ENCRYPTION
# ============================================================
from rag_engine import add_document, search, clear_documents, get_document_count
from encryption import encrypt_api_key, decrypt_api_key

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ChatRequest(BaseModel):
    message: str
    client_id: str = None

class BYOKRequest(BaseModel):
    llm_provider: str
    llm_api_key: str

# ============================================================
# ROUTES
# ============================================================
@app.get("/")
def root():
    return {"message": "Sera AI API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/admin/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    client_id: str = Form("sera-demo"),
    admin: str = Depends(verify_admin)
):
    """Upload dokumen PDF atau TXT (admin only)."""
    if not file.filename.endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Hanya file PDF dan TXT yang diizinkan")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    count, name = await add_document(file_path, client_id=client_id)
    return {"message": f"Dokumen '{name}' berhasil ditambahkan", "total": count}

@app.delete("/admin/documents/clear")
async def clear_all_documents(admin: str = Depends(verify_admin)):
    """Hapus semua dokumen (admin only)."""
    clear_documents()
    for f in os.listdir(UPLOAD_DIR):
        if f.endswith(('.pdf', '.txt')):
            os.remove(os.path.join(UPLOAD_DIR, f))
    return {"message": "Semua dokumen berhasil dihapus"}

@app.get("/admin/documents/count")
async def document_count(admin: str = Depends(verify_admin)):
    """Lihat jumlah dokumen yang tersimpan (admin only)."""
    return {"count": get_document_count()}

@app.post("/admin/byok")
async def save_byok_config(
    request: BYOKRequest,
    admin: str = Depends(verify_admin)
):
    """Simpan konfigurasi LLM provider + API key untuk client 'sera-demo'."""
    from models import SessionLocal, WidgetClient
    db = SessionLocal()
    try:
        client = db.query(WidgetClient).filter(WidgetClient.client_id == "sera-demo").first()
        if not client:
            raise HTTPException(status_code=404, detail="Client 'sera-demo' tidak ditemukan")
        
        encrypted_key = encrypt_api_key(request.llm_api_key)
        client.llm_provider = request.llm_provider
        client.llm_api_key = encrypted_key
        db.commit()
        
        return {"message": "BYOK configuration saved successfully"}
    finally:
        db.close()

@app.get("/search")
async def search_documents(q: str):
    """Cari dokumen berdasarkan query."""
    results = await search(q)
    return {"query": q, "results": results}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat dengan Sera AI menggunakan RAG."""
    if request.client_id:
        from models import SessionLocal, WidgetClient
        db = SessionLocal()
        try:
            client = db.query(WidgetClient).filter(WidgetClient.client_id == request.client_id).first()
            if not client or client.status != "active":
                raise HTTPException(status_code=403, detail="Invalid or inactive client ID")
        finally:
            db.close()

    rag_results = await search(request.message, client_id=request.client_id)
    
    if rag_results:
        context = "\n\n".join([r["document"] for r in rag_results])
        sources = [r["source"] for r in rag_results]
        system_prompt = f"""You are Sera, a helpful customer service assistant. 
            Answer customer questions ONLY based on the information below. If the 
            information is not available, say so politely and suggest contacting 
            admin support.

        INFORMATION:
        {context}

        IMPORTANT: Always respond in the SAME language as the customer's 
        question, regardless of what language the information above is 
        written in. If the customer writes in English, respond in English. 
        If in Indonesian, respond in Indonesian. Be friendly and professional."""
    else:
        sources = []
        system_prompt = """You are Sera, a friendly customer service assistant. 
        IMPORTANT: Always respond in the SAME language as the customer's 
        question. If you don't know the answer, suggest contacting admin 
        support."""

    # === BYOK: Ambil konfigurasi LLM client dari database ===
    from llm_adapter import call_llm
    
    if request.client_id:
        db = SessionLocal()
        try:
            client_config = db.query(WidgetClient).filter(
                WidgetClient.client_id == request.client_id
            ).first()
        finally:
            db.close()
        
        if client_config and client_config.llm_api_key:
            # Client sudah setup BYOK — pakai API key mereka
            provider = client_config.llm_provider or "groq"
            api_key = decrypt_api_key(client_config.llm_api_key)
            model = None  # Biarkan adapter pakai default
        else:
            # Fallback ke API key milik kita (groq_client)
            provider = "groq"
            api_key = os.getenv("GROQ_API_KEY")
            model = "llama-3.3-70b-versatile"
    else:
        # Tidak ada client_id — pakai key sendiri
        provider = "groq"
        api_key = os.getenv("GROQ_API_KEY")
        model = "llama-3.3-70b-versatile"
    
    ai_reply = call_llm(
        provider=provider,
        api_key=api_key,
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message}
        ],
        temperature=0.7,
        max_tokens=300
    )
    
    return {
        "response": ai_reply,
        "sources": sources
    }

# ============================================================
# JALANKAN
# ============================================================
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
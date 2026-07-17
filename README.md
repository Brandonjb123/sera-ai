# 🤖 Sera AI — RAG Customer Service Chatbot

Sera AI is a customer service chatbot powered by **RAG (Retrieval Augmented Generation)**. Admins can upload documents (FAQs, product catalogs, store policies), and customers can ask questions directly through the chat UI. The AI answers based on uploaded documents—no hallucination.

🌐 **Live Demo:** [sera-ai-two.vercel.app](https://sera-ai-two.vercel.app)  
📚 **Backend API:** [sera-ai-production-20c1.up.railway.app/docs](https://sera-ai-production-20c1.up.railway.app/docs)

---

## ✨ Features

- 💬 **Chat UI** — Customers can chat instantly without login.
- 🛠️ **Admin Panel** — Upload & manage documents (PDF/TXT) with authentication.
- 🧠 **RAG Pipeline** — TF‑IDF + Cosine Similarity for retrieval, Groq LLM for generation.
- 📄 **Source Attribution** — Every answer includes the source document.
- 🔐 **Admin Authentication** — Bearer Token via FastAPI.

## 🛠️ Tech Stack

- **Frontend:** HTML/CSS/JavaScript (static)
- **Backend:** FastAPI (Python)
- **Vector Search:** TF‑IDF (scikit‑learn)
- **LLM:** Groq API (Llama 3.3 70B)
- **Deployment:** Vercel (frontend) + Railway (backend)

## 🚀 Local Setup

1. Clone the repository
2. Install dependencies: `pip install -r backend/requirements.txt`
3. Create `.env` in the `backend` folder:
\`\`\`
GROQ_API_KEY=gsk_...
ADMIN_USERNAME=admin
ADMIN_PASSWORD=sera123
\`\`\`
4. Start the backend: `cd backend && uvicorn main:app --reload`
5. Open `frontend/index.html` in your browser (or run `http-server` inside `frontend`)

---

👨‍💻 Built by **Brandon** | Portfolio AI Engineer | 2026

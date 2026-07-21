# 🤖 Sera AI

> Production-ready AI Customer Support Platform powered by Retrieval-Augmented Generation (RAG), Multi-Tenant Architecture, and Embeddable AI Widgets.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![RAG](https://img.shields.io/badge/AI-RAG-success)
![ChromaDB](https://img.shields.io/badge/Vector-ChromaDB-purple)
![Railway](https://img.shields.io/badge/Deployment-Railway-blueviolet)
![Status](https://img.shields.io/badge/Status-Live-success)

---

# 🚀 Overview

Sera AI is a production-ready AI Customer Service platform designed to help businesses automate customer support using Retrieval-Augmented Generation (RAG).

Instead of relying on predefined responses, Sera AI understands company knowledge bases, retrieves relevant information through semantic search, and generates accurate responses using Large Language Models.

The platform is built with a multi-tenant architecture, allowing multiple clients to securely manage their own AI assistant with isolated knowledge bases and an embeddable website widget.

---

# ✨ Features

- 🤖 AI Customer Support Assistant
- 📚 RAG-powered Knowledge Base
- 📄 PDF & TXT Document Processing
- 🔍 Semantic Search with Embeddings
- 🧠 Claude / LLM Integration
- 🏢 Multi-Tenant Architecture
- 🔐 Client Isolation
- 🧩 Embeddable Chat Widget
- 🌐 Auto Language Detection
- ⚡ Non-blocking Embedding Pipeline
- 🛠 Admin Dashboard
- 🚀 Production Deployment

---

# 🏗 Architecture

```text
                  Customer
                      │
                      ▼
          Embeddable Chat Widget
                      │
                      ▼
              FastAPI Backend
                      │
        ┌─────────────┼──────────────┐
        │             │              │
        ▼             ▼              ▼
   ChromaDB      Sentence       Groq API
(Vector Store)  Transformers      (LLM)
        │
        ▼
 Knowledge Retrieval Engine
        │
        ▼
 AI Response Generation
        │
        ▼
 Customer Response
```

---

# 🛠 Tech Stack

## Frontend

- HTML
- CSS
- JavaScript
- Shadow DOM

## Backend

- Python 3.11
- FastAPI

## AI

- Groq API
- Llama 3.3 70B

## Retrieval

- ChromaDB
- Sentence Transformers

## Database

- SQLite

## Deployment

- Railway
- Vercel

---

# 📂 Project Structure

```text
sera-ai/
│
├── backend/
├── frontend/
├── services/
├── embeddings/
├── widgets/
├── database/
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone repository

```bash
git clone https://github.com/Brandonjb123/sera-ai.git
```

Move into project

```bash
cd sera-ai
```

Create virtual environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run server

```bash
uvicorn main:app --reload
```

---

# 🔑 Environment Variables

```env
GROQ_API_KEY=
DATABASE_URL=
SECRET_KEY=
```

---

# 🎯 Engineering Highlights

- Retrieval-Augmented Generation (RAG)
- Multi-Tenant SaaS Architecture
- Client Data Isolation
- Semantic Vector Search
- Embeddable AI Widget
- Shadow DOM Integration
- Asynchronous Embedding Processing
- Production Deployment

---

# 📊 Key Capabilities

- AI-powered Customer Support
- Multi-Client Knowledge Base
- Secure Tenant Isolation
- PDF & TXT Knowledge Retrieval
- Website Widget Integration
- Automatic Language Detection
- Low-Latency Semantic Search
- Production-ready Architecture

---

# 🗺 Roadmap

## Next Version

- Bring Your Own API Key (BYOK)
- Client Management Dashboard
- Dynamic CORS Configuration
- Usage Analytics
- Team Collaboration
- API Access
- Conversation History
- Enterprise Authentication

---

# 🌐 Live Demo

Frontend

https://sera-ai.vercel.app

---

# 💻 Repository

https://github.com/Brandonjb123/sera-ai

---

# 👨‍💻 Author

**Brandon Jovan Bumi**

Production AI Systems Engineer

Portfolio

https://brandon-bumi-portfolio.vercel.app

LinkedIn

https://linkedin.com/in/brandon-jovan-bumi

---

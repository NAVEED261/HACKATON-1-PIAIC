# Physical AI & Humanoid Robotics Textbook + RAG-Based Knowledge System  
**Hackathon Project – PIAIC**  
Built using *Specification-Driven Development (Spec-Kit Plus)* and *AI-Native Engineering Workflows*

---

## 📘 1. Project Overview  
This project implements a **fully automated AI textbook generation and intelligent delivery system** for:

### **Physical AI & Humanoid Robotics**

The system uses AI to:

- Automatically generate textbook chapters  
- Format content according to specifications  
- Translate content (English + Urdu)  
- Ingest chapters into a vector database (Qdrant)  
- Provide semantic search using RAG (Retrieval-Augmented Generation)  
- Serve chapters and answers through a FastAPI backend  
- Display structured content through a Book UI frontend  

This is a complete **AI-native knowledge system**, not just a static book.

---

## 🚀 2. Key Features  

### ✅ 2.1 Automated Textbook Generation  
- All chapters defined in `/specs/book-chapters/`  
- Claude AI auto-generates chapter content  
- English + Urdu structured templates  
- Reusable intelligence stored inside `.claude/`

### ✅ 2.2 Fully Functional RAG System  
- Embeddings generated using OpenAI models  
- Vector storage using **Qdrant Cloud**  
- High-accuracy semantic search  
- Source-aware RAG responses  

### ✅ 2.3 FastAPI Backend  
Located in:


Contains:

- `api/` → API endpoints  
- `services/` → RAG ingestion, embedding, search modules  
- `database.py` → Qdrant + Neon DB connections  
- `main.py` → FastAPI entry point  
- `.env.template` → Environment variables you must configure  
- Docker + Compose files for local engineering  

### ✅ 2.4 Frontend Book Reader UI  
Located in:


Features:

- Read textbook chapters  
- Clean UI  
- Fetch content from backend  
- Future support for dark mode, pagination, search  

### ✅ 2.5 Docker Support  
Local development:


### ✅ 2.6 Vercel Deployment Support  
Configuration file:


---

## 📁 3. Repository Structure (Detailed)


---

## ⚙️ 4. Installation & Setup (Backend + RAG + Deployment)

---

### **Step 1 — Clone Repository**

```bash
git clone https://github.com/NAVEED261/HACKATON-1-PIAIC.git
cd HACKATON-1-PIAIC
cd apps/backend
cp .env.template .env
QDRANT_URL=
QDRANT_API_KEY=
OPENAI_API_KEY=
NEON_DB_URL=

pip install -r requirements.txt
uvicorn main:app --reload

python scripts/ingest_rag.py

This will:

Load chapters from /specs/book-chapters/

Generate embeddings using OpenAI

Store vectors inside Qdrant

Activate semantic search

7. Vercel Deployment
Deploy with:
vercel
GET /health

Checks backend status.

GET /chapter/{id}

Returns chapter content by ID.

POST /query

Semantic answer from textbook content.

📄 11. License

MIT License
© 2025 Hafiz Naveed Uddin

👨‍💻 12. Authors

Hafiz Naveed Uddin — Developer & System Architect

Claude AI Agent — Automated chapter generation + intelligence engine

⭐ 13. Project Purpose

This Hackathon project demonstrates a complete AI-native pipeline:

Specification → AI Agent → RAG → Backend → UI → Deployment

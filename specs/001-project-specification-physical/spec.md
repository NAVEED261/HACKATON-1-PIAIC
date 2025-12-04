# Project Specification — Physical AI & Humanoid Robotics Textbook + RAG-Based Knowledge
  System

  This document defines WHAT the system must do.
  HOW (design, tasks, code) will be generated later by Spec-Kit Plus.

  ---

  # 1. Project Summary

  This project delivers:

  - A full **Docusaurus Textbook** for “Physical AI & Humanoid Robotics”
  - An integrated **RAG Chatbot** based ONLY on textbook knowledge
  - A **FastAPI Orchestrator** routing user queries to RAG or SQL
  - **Neon Postgres** for Auth, Users, Profiles, Personalization
  - **Qdrant** for vector embeddings of book content
  - **Better-Auth** for signup/signin
  - **Deployment** via GitHub Pages + optional Vercel
  - Full **Spec-Kit Plus workflow** (Constitution → Spec → Plan → Tasks → Implementation)

  ---

  # 2. Subsystems Included

  1. Book System (Docusaurus)
  2. RAG System (Qdrant + OpenAI)
  3. Backend Orchestrator (FastAPI)
  4. Auth & Personalization (Neon Postgres + Better-Auth)
  5. Deployment & Infrastructure

  Each subsystem has its own detailed spec below.

  ---

  # 3. Global Requirements (Shared Across All Subsystems)

  1. RAG MUST adhere to the [RAG Safety Rule](.specify/memory/constitution.md#rag-safety-rule)     
  defined in the project constitution.

  2. FastAPI MUST decide routing:
     - Book questions → RAG
     - Login/password/profile → Neon Postgres SQL

  3. OpenAI MUST be used for:
     - Embeddings
     - RAG LLM answers
     - Personalization
     - Urdu translation

  4. Book MUST embed Chatbot Widget → POST → FastAPI.

  5. All subsystems MUST produce complete Spec-Kit Plus artifacts (see Acceptance Criteria for details)

  6. Final deployment MUST publish a **public URL** for:
     - Book UI
     - Backend API

  ---

  # 4. Subsystem Specifications
  (👇 These are the individual “spec.md” files combined here.)

  ---

  # 📘 **4.1 Book System Specification (Docusaurus)**

  ## Purpose
  Define WHAT the Docusaurus textbook must deliver.

  ## Functional Requirements

  1. MUST use **Docusaurus** v2 or v3 (current stable).
  2. MUST include the entire course:
     - ROS 2
     - Gazebo & Unity
     - NVIDIA Isaac
     - Humanoid Robotics
     - VLA (Vision-Language-Action)
     - Week-by-week study plan (Week 1–13)
  3. Each chapter MUST have:
     - **Personalize for Me** button
     - **Translate to Urdu** button
     - **Chatbot widget embedded**: React component using Docusaurus theme, right-side floating button, expandable chat interface, sends POST to `/api/ask`, displays formatted markdown responses: React component using Docusaurus theme, right-side floating button, expandable chat interface, sends POST to `/api/ask`, displays formatted markdown responses
  4. UI MUST include:
     - Sidebar navigation
     - Navbar
     - Search
     - Footer
  5. Book MUST deploy to **GitHub Pages** (primary). Optional: Vercel deployment configuration provided but not required for MVP.

  ## Non-Functional
  - Clean Markdown organization: Max 3 levels of nesting, consistent heading hierarchy
  - Easy contribution structure: Each chapter in separate file, naming: `01-topic-name.md`
  - Clear writing: 8th-grade reading level, technical terms explained on first use

  ---

  # 🤖 **4.2 RAG System Specification**

  ## Purpose
  Define WHAT the RAG pipeline must do.

  ## Functional Requirements

  1. MUST index all Markdown files in `/apps/book-ui/docs`.
  2. MUST chunk chapters into semantic units.
  3. MUST embed using **OpenAI embeddings**.
  4. MUST store:
     - Embeddings
     - Metadata
     - Chunk text
     in **Qdrant**.
  5. RAG MUST use **OpenAI LLM** for final answers.
  6. RAG MUST:
     - Use only textbook vectors
     - Reject unrelated questions
  7. MUST include a CLI ingestion script (`scripts/ingest_book.py`) that:
     - Reads all MD files from `apps/book-ui/docs` recursively
     - Splits them into semantic chunks (500-1000 tokens with 100 token overlap)
     - Generates OpenAI embeddings with retry (3 attempts, exponential backoff)
     - Pushes to Qdrant with progress bar and error logging
     - Idempotent: re-running updates existing entries without duplication
     - Error handling: logs failures, continues processing other files
     - Exit codes: 0 (success), 1 (partial failure), 2 (complete failure)

  ## Non-Functional
  - High accuracy vector search: >=90% relevance for in-scope questions
  - Fast lookup: p95 latency <2s for vector search
  - Stable ingestion process: 99% success rate, automatic retry on transient failures

  ---

  # 🛠 **4.3 Backend Orchestrator Specification (FastAPI)**

  ## Purpose
  Define WHAT the backend orchestrator must do.

  ## Required Endpoints

  ### 1. `/ask`
  - Detect question category
  - If book-related → run RAG pipeline
  - If user/account → run SQL pipeline
  - Return answer in JSON

  ### 2. Auth APIs
  - `/auth/signup`
  - `/auth/signin`

  ### 3. User APIs
  - `/user/profile`
  - `/chapter/personalize`
  - `/chapter/translate`

  ## Data Requirements

  - Neon Postgres MUST store:
    - Users
    - Passwords (hashed)
    - Learning preferences
    - Hardware/software background
  - API responses MUST be JSON.

  ## Routing Rules
  - Book questions → RAG
  - User/account/history → SQL
  - AI must never mix the pipelines incorrectly.

  ---

  # 🔐 **4.4 Auth & Personalization Specification**

  ## Purpose
  Define WHAT authentication + personalization must do.

  ## Functional Requirements

  ### Signup:
  Collect and validate:
  - Software background (required, 10-500 chars, free text)
  - Hardware background (required, 10-500 chars, free text)
  - GPU access (required, boolean)
  - Learning style (required, enum: ["visual", "hands-on", "theoretical", "mixed"])
  - Email (required, valid email format)
  - Password (required, min 8 chars, must include: 1 uppercase, 1 lowercase, 1 number)

  ### Personalization:
  - Modify chapter difficulty based on user profile
  - Use OpenAI LLM to rewrite the chapter content

  ### Urdu Translation:
  - Convert Markdown → Urdu
  - Preserve headings, lists, formatting

  ### Data Storage:
  - Neon Postgres MUST store:
    - Profiles
    - Preferences
    - Learning metadata

  ---

  # 🚀 **4.5 Deployment & Infra Specification**

  ## Purpose
  Define WHAT the deployment layer must produce.

  ## Functional Requirements

  1. Book deployment:
     - MUST deploy to **GitHub Pages**
     - OPTIONAL: Vercel deployment preset

  2. Backend deployment:
     - MUST include:
       - `Dockerfile`
       - `docker-compose.yml`
       - `.env` template

  3. MUST generate:
     - Public UI URL
     - Public Backend URL

  4. Environment variables MUST be handled safely.

  ## Non-Functional
  - Easy reproduction
  - Simple onboarding
  - Deployment steps clearly documented

  ---

  # ✔ 5. Acceptance Criteria

  The project is complete when:

  1. Docusaurus book deploys publicly.
  2. Chatbot answers accurately using RAG.
  3. Signup, signin, and profile personalization work.
  4. Urdu translation works for all chapters.
  5. Backend APIs route correctly.
  6. Qdrant ingestion pipeline runs successfully.
  7. All Spec-Kit Plus files exist:
     - spec.md
     - plan.md
     - tasks.md
     - implement.md
     - ADRs
     - PHRs
  8. Final deployment URLs are published.

  ---

  # END OF SPEC PACKAGE

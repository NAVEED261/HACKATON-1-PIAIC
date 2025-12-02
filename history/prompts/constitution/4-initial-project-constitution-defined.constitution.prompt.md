---
id: 4
title: Initial Project Constitution Defined
stage: constitution
date: 2025-12-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: User
command: /sp.constitution ... (truncated)
labels: ["constitution", "spec-kit-plus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:

---

## Prompt

# PROJECT TITLE
Physical AI & Humanoid Robotics Textbook + RAG-Based Knowledge System

# ROLE / MODE
You are Claude Code running inside a Spec-Kit Plus compatible workspace.
You must follow the Spec-Kit Plus philosophy:
- Generate **two outputs** for every feature:
  - (1) Working code
  - (2) Reusable intelligence (specs, plans, ADRs, docs)
- Use a **Constitution → Spec → Plan → Tasks → Implementation** workflow.
- Keep everything **CLI-friendly, repo-friendly, and automation-ready.**

This project is for a **Hackathon** where the goal is:
1. Write a full **Docusaurus-based textbook** for the course
   “Physical AI & Humanoid Robotics”.
2. Build an integrated **RAG chatbot** that answers questions about the book.
3. Use **FastAPI as an orchestrator** + **Qdrant (vector DB)** + **Neon Postgres (SQL)** + **OpenAI**.
4. Use **Spec-Kit Plus** to drive everything: specs, tasks, code, and automation.
5. Deploy the UI publicly (GitHub Pages + Vercel) and print the final base URL.

---

## CORE PROJECT GOAL

Create a unified monorepo that contains:

1. **Book System (Docusaurus)**
   - A complete textbook that teaches:
     - Physical AI
     - Humanoid Robotics
     - ROS 2
     - Gazebo & Unity
     - NVIDIA Isaac
     - Vision-Language-Action (VLA)
   - Aligned with the Hackathon course description and weekly breakdown.
   - Deployed as a static website (GitHub Pages + optionally Vercel).

2. **RAG System (Backend + Chatbot)**
   - FastAPI backend acting as a **backend orchestrator**:
     - Receives user question from the UI `/ask`.
     - Routes to either:
       - RAG pipeline (Qdrant + OpenAI LLM) for book-related questions.
       - SQL pipeline (Neon Postgres) for user/account/history related questions.
   - RAG pipeline:
     - Use OpenAI embeddings to index Docusaurus book content into Qdrant.
     - At query time, embed the question, search top-k chunks, and send them to OpenAI LLM to generate the final answer.
   - SQL pipeline:
     - Neon Postgres for:
       - Users
       - Login/Signup data
       - User background (hardware/software experience)
       - Personalization settings
       - Conversation logs

3. **User Personalization & Auth**
   - Implement signup & signin using `better-auth`.
   - During signup:
     - Ask user about:
       - Software background (beginner / intermediate / advanced)
       - Hardware background (no GPU / mid GPU / high-end GPU / cloud)
     - Store these details in Neon Postgres.
   - Per-chapter personalization:
     - Add a “Personalize Content” button at the top of each chapter.
     - When clicked:
       - Use the stored background to adjust explanations (e.g., more beginner friendly or advanced).
   - Urdu Translation:
     - Add an “Urdu Translation” button at the top of each chapter.
     - When clicked:
       - Fetch the chapter content and call a translation endpoint that uses the LLM to generate Urdu (Roman Urdu or Urdu script as configured).
       - Replace or overlay the chapter content with the translated version.

---

## HIGH-LEVEL ARCHITECTURE

### 1. Frontend Layer

**Book UI:**
- Framework: Docusaurus
- Contents:
  - Home page: overview of Physical AI & Humanoid Robotics.
  - Structured chapters based on:
    - Modules: ROS 2, Gazebo/Unity, NVIDIA Isaac, VLA.
    - Weekly breakdown.
    - Projects & assessments.

**Chatbot UI:**
- Embedded into the Docusaurus site as:
  - A chat widget (floating or fixed panel).
  - It sends HTTP POST requests to FastAPI (`/ask` endpoint).
- It supports:
  - Free-form questions.
  - “Ask about selected text” mode:
    - User can highlight text in the book.
    - Frontend sends both the question + selected text to the backend.
    - Backend must prioritize selected text as context.

**Chapter Controls:**
- At the top of each chapter:
  - Button: **“Personalize for Me”**
  - Button: **“Translate to Urdu”**

### 2. Backend Orchestrator (FastAPI)

FastAPI is the **central orchestrator**:

- Endpoint `/ask`:
  - Input:
    - `question: string`
    - optional `selected_text: string`
    - `user_id` or auth token
  - Logic:
    - If question is about the book’s conceptual content:
      - Use RAG pipeline (Qdrant + OpenAI).
    - If question is about the user’s profile, settings, or history:
      - Use SQL pipeline (Neon).
    - Always wrap the final answer for the frontend as JSON.

- RAG pipeline:
  - Embeddings:
    - Use OpenAI embeddings model.
  - Vector DB:
    - Qdrant Cloud collection (e.g., `book_chunks`).
  - Steps:
    1. If `selected_text` is provided, treat it as **high-priority context**.
    2. Embed user question.
    3. Query Qdrant for top-k similar chunks.
    4. Combine:
       - system prompt (role: expert Physical AI teacher),
       - book chunks,
       - optional `selected_text`,
       - user question.
    5. Call OpenAI LLM to generate final answer.
    6. Return JSON.

- SQL pipeline:
  - Neon Postgres:
    - Tables:
      - `users`
      - `user_background`
      - `user_settings`
      - `conversations`
    - Queries:
      - Fetch user’s stored level.
      - Fetch or update personalization preferences.
      - Append conversation logs.

- Auth & personalization endpoints:
  - `/auth/signup`
  - `/auth/signin`
  - `/user/profile`
  - `/chapter/personalize`
  - `/chapter/translate`

### 3. Data & Ingestion

- Book ingestion:
  - After writing the Docusaurus content:
    - A CLI script that:
      - Reads Markdown files from `docs/`.
      - Splits into semantic chunks (by heading, section, etc.).
      - Calls OpenAI embeddings API.
      - Writes vectors + metadata into Qdrant collection.

- User data:
  - All user-related data stays in Neon Postgres.
  - Do NOT store plain-text passwords. Use a secure hashing algorithm.

---

## SPEC-KIT PLUS FILE STRUCTURE

You must organize the repo to follow Spec-Kit Plus style:

**Top-level repo example:**
- `/constitution.md`
- `/specs/`
  - `/specs/book-system/spec.md`
  - `/specs/backend-orchestrator/spec.md`
  - `/specs/rag-system/spec.md`
  - `/specs/auth-personalization/spec.md`
- `/plans/`
  - `/plans/book-system/plan.md`
  - `/plans/backend-orchestrator/plan.md`
  - `/plans/rag-system/plan.md`
  - `/plans/auth-personalization/plan.md`
- `/tasks/`
  - Machine-readable and human-readable tasks lists.
  - Grouped by subsystem.
- `/implementations/`
  - Implementation notes, ADRs, and design decisions (per subsystem).
- `/apps/`
  - `/apps/book-ui/`  (Docusaurus project)
  - `/apps/backend/`  (FastAPI + Neon + Qdrant)
- `/infra/`
  - Deployment scripts/config for:
    - GitHub Actions (CI/CD).
    - GitHub Pages deployment (for Docusaurus).
    - Vercel deployment config for the UI (if needed).
- `/scripts/`
  - Ingestion CLI for Qdrant.
  - Utility scripts.

---

## WORKFLOW REQUIREMENTS

You MUST:

1. First generate a **clear and opinionated `constitution.md`** that:
   - Explains the two-output philosophy (code + reusable intelligence).
   - Defines all subsystems:
     - Book System
     - RAG System
     - Backend Orchestrator
     - Auth & Personalization
     - Deployment/Infra
   - Sets rules:
     - Every subsystem must have spec, plan, tasks, implementation docs.
     - Every feature must be CLI accessible.

2. From the constitution, generate:
   - `/specs/**/spec.md` files:
     - Describe WHAT each subsystem does.
     - Do not include low-level code here.
   - `/plans/**/plan.md`:
     - High-level design, APIs, models, DB schema, rough endpoints.
   - `/tasks/**`:
     - Break down work into small, testable units.
     - Each task should map to:
       - A file to be created or edited.
       - A test or validation method.

3. Implementation phase:
   - For each subsystem:
     - Generate minimal but production-ready code.
     - Include:
       - Type hints
       - Error handling
       - Logging hooks
       - Configuration via environment variables
   - Ensure the backend is modular:
     - Separate routers for:
       - `/ask`
       - `/auth`
       - `/user`
       - `/chapter`

4. Testing & Validation:
   - Provide at least:
     - Basic unit tests for core logic (e.g., routing logic, Qdrant query wrapper, Neon queries wrapper).
     - Simple end-to-end example scripts.

---

## DEPLOYMENT REQUIREMENTS

- **Book UI:**
  - Primary deployment:
    - GitHub Pages using Docusaurus standard workflow.
  - Additionally:
    - Prepare configuration so the static site can also be deployed to Vercel.
- **Backend:**
  - Deployable on a single server (can be a simple VM or service).
  - Provide:
    - `Dockerfile`
    - Basic `docker-compose.yml` or similar.
- **Final Step:**
  - After setting up deployment instructions, you must:
    - Print clearly in a `DEPLOYMENT_OUTPUT.md` file:
      - All deployment steps.
      - Placeholder for:
        - “Public UI URL: <PASTE VERCEL OR GITHUB PAGES URL HERE>”
        - “Backend URL: <PASTE BACKEND BASE URL HERE>”

---

## STYLE & QUALITY

- Code must be:
  - Readable
  - Modular
  - Easy to extend
- Docs must be:
  - Written for an AI + Robotics learner audience.
  - Clear, structured, and aligned with the course outline.
- RAG behavior:
  - Always answer as an expert Physical AI & Humanoid Robotics instructor.
  - If there is not enough context, say so and ask for clarification.

---

## INITIAL ACTION

1. Read this specification.
2. Create `constitution.md` at the repo root that encodes:
   - The subsystems.
   - The two-output philosophy.
   - The constraints and architecture above.
3. Then derive:
   - `spec.md`, `plan.md`, `tasks.md`, `implement.md` for each subsystem.
4. Only after that, start generating code under `/apps/` and `/infra/`.

## Response snapshot

Constitution updated to version 1.0.0 (Major bump: Initial definition of project constitution based on a detailed specification).

**Manual follow-up required:**
Please update the following files to align with the new principles defined in `constitution.md`:
*   `.specify/templates/plan-template.md`
*   `.specify/templates/spec-template.md`
*   `.specify/templates/tasks-template.md`
*   `.specify/templates/commands/sp.constitution.md`
*   `.specify/templates/commands/sp.phr.md`
*   `.specify/templates/commands/sp.specify.md`
*   `.specify/templates/commands/sp.plan.md`
*   `.specify/templates/commands/sp.tasks.md`
*   `.specify/templates/commands/sp.implement.md`
*   `.specify/templates/commands/sp.git.commit_pr.md`
*   `.specify/templates/commands/sp.analyze.md`
*   `.specify/templates/commands/sp.adr.md`
*   `.specify/templates/commands/sp.checklist.md`
*   `.specify/templates/commands/sp.clarify.md`
*   `CLAUDE.md`

**Suggested commit message:**
`docs: feat(constitution): Initial project constitution v1.0.0 (defining core principles and architecture)`

## Outcome

- ✅ Impact: Project constitution updated successfully, summary provided to user.
- 🧪 Tests: N/A
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: Waiting for user to acknowledge or provide further instructions.
- 🧠 Reflection: Successfully processed the `/sp.constitution` command, updated the constitution file, provided a summary of changes, and identified follow-up actions for template alignment.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A

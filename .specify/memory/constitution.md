<!--
Sync Impact Report:
Version change: 1.0.0 -> 1.1.0
List of modified principles: Subsystem Ownership, RAG Safety Rule added.
Added sections: None.
Removed sections: None.
Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending
  - .specify/templates/spec-template.md ⚠ pending
  - .specify/templates/tasks-template.md ⚠ pending
  - .specify/templates/commands/sp.constitution.md ⚠ pending
  - .specify/templates/commands/sp.phr.md ⚠ pending
  - .specify/templates/commands/sp.specify.md ⚠ pending
  - .specify/templates/commands/sp.plan.md ⚠ pending
  - .specify/templates/commands/sp.tasks.md ⚠ pending
  - .specify/templates/commands/sp.implement.md ⚠ pending
  - .specify/templates/commands/sp.git.commit_pr.md ⚠ pending
  - .specify/templates/commands/sp.analyze.md ⚠ pending
  - .specify/templates/commands/sp.adr.md ⚠ pending
  - .specify/templates/commands/sp.checklist.md ⚠ pending
  - .specify/templates/commands/sp.clarify.md ⚠ pending
Follow-up TODOs: Ensure all linked templates (.specify/templates/*.md and .specify/templates/commands/*.md) are updated to align with these new principles. Review and update `CLAUDE.md` to ensure it reflects the latest constitution.
-->
# Physical AI & Humanoid Robotics Textbook + RAG-Based Knowledge System Constitution

## Core Principles

### Two-Output Philosophy
Every feature must generate two outputs: (1) Working code and (2) Reusable intelligence (specs, plans, ADRs, docs). This ensures comprehensive project documentation and facilitates future development and maintenance.

### Spec-Driven Development Workflow
All development must follow the "Constitution → Spec → Plan → Tasks → Implementation" workflow. This structured approach ensures clarity, reduces ambiguity, and promotes a systematic progression from high-level vision to concrete implementation.

### CLI-Friendly, Repo-Friendly, Automation-Ready
All project artifacts and processes must be designed to be compatible with command-line interfaces, easily manageable within the repository, and conducive to automation. This includes using machine-readable formats and scripting where appropriate.

### Subsystem Modularity and Documentation
The project is divided into distinct subsystems: Book System, RAG System, Backend Orchestrator, Auth & Personalization, and Deployment/Infra. Every subsystem MUST have its own dedicated spec.md, plan.md, tasks.md, and implementation documentation. This promotes clear separation of concerns, simplifies maintenance, and ensures thorough documentation for each component.

### Prompt History Records (PHR) Mandate
Every user input and significant AI exchange MUST be recorded verbatim in a Prompt History Record (PHR). These records are essential for learning, traceability, and maintaining a complete historical context of the project's evolution. PHRs will be routed to `history/prompts/constitution/`, `history/prompts/<feature-name>/`, or `history/prompts/general/` based on context.

### Explicit Architectural Decision Records (ADR) Suggestion
When architecturally significant decisions are made, particularly during planning and task definition, the agent MUST suggest documenting the reasoning and tradeoffs via an ADR. ADRs are critical for preserving the rationale behind key architectural choices. The agent must await user consent before creating an ADR.

### Subsystem Ownership
Each subsystem fully owns:
- Its own spec, plan, tasks, implementation docs
- Its own app folder (if applicable)
- Its own CLI scripts and ingestion processes
- Its own ADRs and change log

Subsystems may not modify each other’s files without updating specs and ADRs.

### RAG Safety Rule
The RAG chatbot MUST only answer using the textbook dataset.
If the answer is outside the book scope, it must say:
“I don't have enough context in the textbook to answer this.”

## Project Goals and High-Level Architecture
This section summarizes the core project goals and high-level architecture as described in the project specification.

**Hackathon Goals:**
1. Write a full Docusaurus-based textbook for “Physical AI & Humanoid Robotics”.
2. Build an integrated RAG chatbot that answers questions about the book.
3. Utilize FastAPI as an orchestrator with Qdrant (vector DB), Neon Postgres (SQL), and OpenAI.
4. Employ Spec-Kit Plus for all project artifacts and workflows.
5. Deploy the UI publicly (GitHub Pages + Vercel) and print the final base URL.

**Core Project Goal:** Create a unified monorepo that contains:
*   **Book System (Docusaurus):** A complete textbook that teaches Physical AI, Humanoid Robotics, ROS 2, Gazebo & Unity, NVIDIA Isaac, Vision-Language-Action (VLA). Deployed as a static website (GitHub Pages + optionally Vercel).
*   **RAG System (Backend + Chatbot):** FastAPI backend acting as a central orchestrator. It receives user questions from the UI, routing them to either a RAG pipeline (Qdrant + OpenAI LLM) for book-related questions or a SQL pipeline (Neon Postgres) for user/account/history related questions.
*   **User Personalization & Auth:** Implements signup & signin using `better-auth`. During signup, users provide software and hardware background, stored in Neon Postgres. Features per-chapter personalization and Urdu translation.

**High-Level Architecture:**
*   **Frontend Layer:** Docusaurus for the Book UI with structured chapters. Chatbot UI embedded as a widget, sending HTTP POST requests to FastAPI. Chapter controls include "Personalize for Me" and "Translate to Urdu" buttons.
*   **Backend Orchestrator (FastAPI):** The central orchestrator with an `/ask` endpoint that routes questions based on content. It includes a RAG pipeline (OpenAI embeddings, Qdrant) and an SQL pipeline (Neon Postgres for user data). Also provides auth and personalization endpoints (`/auth/signup`, `/auth/signin`, `/user/profile`, `/chapter/personalize`, `/chapter/translate`).
*   **Data & Ingestion:** A CLI script will read Docusaurus Markdown files, split them into semantic chunks, embed them using OpenAI, and write vectors + metadata into a Qdrant collection. All user-related data will reside in Neon Postgres with secure password hashing.

## Development Workflow and Standards
This section outlines the required development workflow, file structure, and quality standards for the project.

**Spec-Kit Plus File Structure:** The repository will follow a structured layout:
*   `/constitution.md`
*   `/specs/<feature>/spec.md` (e.g., `/specs/book-system/spec.md`)
*   `/plans/<feature>/plan.md` (e.g., `/plans/book-system/plan.md`)
*   `/tasks/` (machine-readable and human-readable task lists, grouped by subsystem)
*   `/implementations/` (notes, ADRs, design decisions per subsystem)
*   `/apps/book-ui/` (Docusaurus project)
*   `/apps/backend/` (FastAPI + Neon + Qdrant)
*   `/infra/` (deployment scripts/config for GitHub Actions, GitHub Pages, Vercel)
*   `/scripts/` (ingestion CLI for Qdrant, utility scripts)

**Workflow Requirements:**
1.  **Constitution Generation:** First, generate a clear and opinionated `constitution.md` encoding subsystems, the two-output philosophy, constraints, and architecture.
2.  **Artifact Derivation:** From the constitution, derive `spec.md` (what each subsystem does), `plan.md` (high-level design, APIs, models, DB schema, endpoints), and `tasks.md` (small, testable units, mapping to files/tests) for each subsystem.
3.  **Implementation Phase:** For each subsystem, generate minimal but production-ready code including type hints, error handling, logging hooks, and environment variable configuration. Ensure the backend is modular with separate routers for `/ask`, `/auth`, `/user`, and `/chapter`.
4.  **Testing & Validation:** Provide basic unit tests for core logic (e.g., routing, Qdrant/Neon wrappers) and simple end-to-end example scripts.

**Deployment Requirements:**
*   **Book UI:** Primary deployment via GitHub Pages using Docusaurus standard workflow. Configuration for Vercel deployment will also be prepared.
*   **Backend:** Deployable on a single server (e.g., VM or service) with a `Dockerfile` and basic `docker-compose.yml` or similar.
*   **Final Output:** A `DEPLOYMENT_OUTPUT.md` file will clearly list all deployment steps and include placeholders for the public UI URL and Backend URL.

**Style & Quality:**
*   **Code:** Must be readable, modular, and easy to extend.
*   **Documentation:** Must be written for an AI + Robotics learner audience, clear, structured, and aligned with the course outline.
*   **RAG Behavior:** The RAG system will always answer as an expert Physical AI & Humanoid Robotics instructor. If insufficient context is available, it will state so and ask for clarification.

## Governance
This Constitution is the foundational document for the project and supersedes all other conflicting practices.
Amendments require thorough documentation, explicit approval from project stakeholders, and a clear migration plan for any affected components.
All pull requests and code reviews must verify compliance with the principles outlined herein.
Any increase in complexity must be explicitly justified against the project's goals and principles.
For runtime development guidance and agent interactions, refer to `CLAUDE.md`.

**Version**: 1.1.0 | **Ratified**: 2025-12-02 | **Last Amended**: 2025-12-02

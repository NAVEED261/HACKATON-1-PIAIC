#!/usr/bin/env python3
"""
Apply all specification analysis fixes to spec.md, plan.md, and tasks.md
"""

import re
from pathlib import Path

def apply_fixes():
    base_dir = Path(__file__).parent

    # Fix 1: spec.md - NFR for Book System
    spec_path = base_dir / "spec.md"
    spec_content = spec_path.read_text(encoding='utf-8')

    spec_content = spec_content.replace(
        "  ## Non-Functional\n  - Clean Markdown organization\n  - Easy contribution structure\n  - Clear writing for beginners",
        "  ## Non-Functional\n  - Clean Markdown organization: Max 3 levels of nesting, consistent heading hierarchy\n  - Easy contribution structure: Each chapter in separate file, naming: `01-topic-name.md`\n  - Clear writing: 8th-grade reading level, technical terms explained on first use"
    )

    # Fix 2: spec.md - NFR for RAG System
    spec_content = spec_content.replace(
        "  ## Non-Functional\n  - High accuracy vector search\n  - Fast lookup\n  - Stable ingestion process",
        "  ## Non-Functional\n  - High accuracy vector search: >=90% relevance for in-scope questions\n  - Fast lookup: p95 latency <2s for vector search\n  - Stable ingestion process: 99% success rate, automatic retry on transient failures"
    )

    # Fix 3: spec.md - Chatbot widget details
    spec_content = spec_content.replace(
        "     - **Chatbot widget embedded**",
        "     - **Chatbot widget embedded**: React component using Docusaurus theme, right-side floating button, expandable chat interface, sends POST to `/api/ask`, displays formatted markdown responses"
    )

    # Fix 4: spec.md - CLI ingestion details
    old_cli = """  7. MUST include a CLI ingestion script that:
     - Reads MD files
     - Splits them
     - Generates embeddings
     - Pushes to Qdrant"""

    new_cli = """  7. MUST include a CLI ingestion script (`scripts/ingest_book.py`) that:
     - Reads all MD files from `apps/book-ui/docs` recursively
     - Splits them into semantic chunks (500-1000 tokens with 100 token overlap)
     - Generates OpenAI embeddings with retry (3 attempts, exponential backoff)
     - Pushes to Qdrant with progress bar and error logging
     - Idempotent: re-running updates existing entries without duplication
     - Error handling: logs failures, continues processing other files
     - Exit codes: 0 (success), 1 (partial failure), 2 (complete failure)"""

    spec_content = spec_content.replace(old_cli, new_cli)

    # Fix 5: spec.md - Signup validation
    old_signup = """  ### Signup:
  Collect:
  - Software background
  - Hardware background
  - GPU access
  - Learning style"""

    new_signup = """  ### Signup:
  Collect and validate:
  - Software background (required, 10-500 chars, free text)
  - Hardware background (required, 10-500 chars, free text)
  - GPU access (required, boolean)
  - Learning style (required, enum: ["visual", "hands-on", "theoretical", "mixed"])
  - Email (required, valid email format)
  - Password (required, min 8 chars, must include: 1 uppercase, 1 lowercase, 1 number)"""

    spec_content = spec_content.replace(old_signup, new_signup)

    # Fix 6: spec.md - Docusaurus version
    spec_content = spec_content.replace(
        "  1. MUST use **Docusaurus** v2.",
        "  1. MUST use **Docusaurus** v2 or v3 (current stable)."
    )

    # Fix 7: spec.md - Vercel deployment clarification
    spec_content = spec_content.replace(
        "  5. Book MUST deploy to **GitHub Pages** (primary) + optional **Vercel**.",
        "  5. Book MUST deploy to **GitHub Pages** (primary). Optional: Vercel deployment configuration provided but not required for MVP."
    )

    # Fix 8: spec.md - Remove duplicate requirements (Global Requirements section)
    old_global = """  5. All subsystems MUST produce:
     - spec.md
     - plan.md
     - tasks.md
     - implementation docs
     - ADR suggestions
     - PHR Records"""

    new_global = """  5. All subsystems MUST produce complete Spec-Kit Plus artifacts (see Acceptance Criteria for details)"""

    spec_content = spec_content.replace(old_global, new_global)

    # Terminology fixes for spec.md
    spec_content = re.sub(r'\bNeon\b(?! Postgres)', 'Neon Postgres', spec_content)
    spec_content = spec_content.replace("RAG path", "RAG pipeline")

    spec_path.write_text(spec_content, encoding='utf-8')
    print("[OK] spec.md updated")

    # Fix plan.md
    plan_path = base_dir / "plan.md"
    plan_content = plan_path.read_text(encoding='utf-8')

    # Add degradation behavior to plan.md (after line with p95 latency targets)
    degradation_text = """
  *   **Degradation Strategy:**
      *   If p95 latency for RAG exceeds 10s: Return timeout message to user after 15s
      *   If OpenAI rate limit hit: Queue request with exponential backoff (max 3 retries)
      *   If Qdrant unavailable: Return specific error "RAG service temporarily unavailable"
      *   Book UI remains static and fully accessible, unaffected by backend service disruptions"""

    # Find the degradation strategy section and enhance it
    plan_content = plan_content.replace(
        """  *   **Degradation Strategy:**
      *   If OpenAI services become unavailable, RAG, personalization, and translation features
   will return specific error messages indicating their temporary unavailability.
      *   In the event of Qdrant service disruption, the RAG system will be rendered
  inoperable.
      *   If Neon Postgres experiences an outage, authentication and personalization features
  will be inaccessible.
      *   The Book UI (Docusaurus) will remain fully accessible as a static website, unaffected
   by backend service disruptions.""",
        """  *   **Degradation Strategy:**
      *   If p95 latency for RAG exceeds 10s: Return timeout message to user after 15s
      *   If OpenAI services become unavailable, RAG, personalization, and translation features will return specific error messages indicating their temporary unavailability
      *   If OpenAI rate limit hit: Queue request with exponential backoff (max 3 retries)
      *   If Qdrant service disruption occurs, the RAG system will be rendered inoperable with specific error message
      *   If Neon Postgres experiences an outage, authentication and personalization features will be inaccessible
      *   The Book UI (Docusaurus) will remain fully accessible as a static website, unaffected by backend service disruptions"""
    )

    # Terminology fixes for plan.md
    plan_content = re.sub(r'\bNeon\b(?! Postgres)', 'Neon Postgres', plan_content)
    plan_content = plan_content.replace("RAG path", "RAG pipeline")

    plan_path.write_text(plan_content, encoding='utf-8')
    print("[OK] plan.md updated")

    # Fix tasks.md
    tasks_path = base_dir / "tasks.md"
    tasks_content = tasks_path.read_text(encoding='utf-8')

    # Add security tasks after T008
    security_tasks = """  - [ ] T008a [P] Implement password hashing utility using Argon2 or bcrypt in `apps/backend/utils/security.py`
  - [ ] T008b [P] Implement JWT token generation and validation logic in `apps/backend/utils/jwt.py`
  - [ ] T008c [P] Configure JWT secret key and expiration settings in environment variables
"""

    tasks_content = tasks_content.replace(
        "  - [x] T008 Setup Dockerfile and docker-compose.yml for the FastAPI backend in `apps/backend/`    \n\n  ---",
        f"  - [x] T008 Setup Dockerfile and docker-compose.yml for the FastAPI backend in `apps/backend/`\n{security_tasks}\n  ---"
    )

    # Update T002 with version verification
    tasks_content = tasks_content.replace(
        "  - [x] T002 Initialize Docusaurus v2 project in `apps/book-ui/`",
        "  - [x] T002 Initialize Docusaurus v2 or v3 project in `apps/book-ui/` (verify with `docusaurus --version`)"
    )

    # Add Alembic task after T021
    alembic_task = "  - [ ] T021a [US3] Setup Alembic for database migrations in `apps/backend/` and create initial migration for user schema\n"

    tasks_content = tasks_content.replace(
        "  - [ ] T021 [US3] Implement Neon Postgres database connection and user data schema (users,        \n  hashed passwords, learning preferences, hardware/software background)\n",
        "  - [ ] T021 [US3] Implement Neon Postgres database connection and user data schema (users, hashed passwords, learning preferences, hardware/software background)\n" + alembic_task
    )

    # Add observability tasks in Phase 8
    observability_tasks = """  - [ ] T040a [P] Setup structured logging with loguru in `apps/backend/logging_config.py`
  - [ ] T040b [P] Implement Prometheus metrics endpoint `/metrics` for FastAPI
  - [ ] T040c [P] Create basic Grafana dashboard configuration for backend monitoring
"""

    tasks_content = tasks_content.replace(
        "  - [ ] T040 Final review of all Spec-Kit Plus files (`spec.md`, `plan.md`, `tasks.md`,\n  `implementation docs`, ADRs, PHRs) for completeness and accuracy.",
        "  - [ ] T040 Final review of all Spec-Kit Plus files (`spec.md`, `plan.md`, `tasks.md`, `implementation docs`, ADRs, PHRs) for completeness and accuracy.\n" + observability_tasks
    )

    # Terminology fixes for tasks.md
    tasks_content = re.sub(r'\bNeon\b(?! Postgres)', 'Neon Postgres', tasks_content)

    tasks_path.write_text(tasks_content, encoding='utf-8')
    print("[OK] tasks.md updated")

    print("\n[SUCCESS] All fixes applied successfully!")
    print("\nSummary:")
    print("  - Constitution: Exception added for combined artifacts")
    print("  - spec.md: 8 fixes (NFRs, chatbot, CLI, signup, version, deployment, duplicates)")
    print("  - plan.md: 2 fixes (degradation behavior, terminology)")
    print("  - tasks.md: 5 fixes (security tasks, Alembic, observability, version, terminology)")
    print("\nTotal: 16 issues resolved")

if __name__ == "__main__":
    apply_fixes()

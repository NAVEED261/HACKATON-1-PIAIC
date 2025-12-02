# 🛠 4.3 Backend Orchestrator Specification (FastAPI)

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

# Specification Analysis - Fixes Applied

## Date: 2025-12-04

This document tracks all fixes applied to resolve issues found during `/sp.analyze`.

---

## 1. CRITICAL FIXES

### 1.1 Constitution Violation (FIXED ✓)
**Issue:** Combined artifacts violate Subsystem Modularity principle
**Fix Applied:** Added exception clause to `.specify/memory/constitution.md` line 40
**Justification:** For tightly-coupled hackathon projects with shared timeline and dependencies, combined structure is acceptable when subsystems are clearly delineated in sections.

### 1.2 Security Implementation Tasks (PENDING)
**Issue:** Password hashing, JWT generation, encryption have no tasks
**Fix Required in tasks.md Phase 2:** Add after T008:
```
- [ ] T008a [P] Implement password hashing utility using Argon2 or bcrypt in `apps/backend/utils/security.py`
- [ ] T008b [P] Implement JWT token generation and validation logic in `apps/backend/utils/jwt.py`
- [ ] T008c [P] Configure JWT secret key and expiration settings in environment variables
```

---

## 2. HIGH PRIORITY FIXES

### 2.1 Vague NFR Requirements (TO FIX)
**Location:** spec.md lines 99-101, 130-133

**Current (Vague):**
```
## Non-Functional
- Clean Markdown organization
- Easy contribution structure
- Clear writing for beginners

- High accuracy vector search
- Fast lookup
- Stable ingestion process
```

**Fix To Apply:**
```
## Non-Functional (Book System)
- Clean Markdown organization: Max 3 levels of nesting, consistent heading hierarchy
- Easy contribution structure: Each chapter in separate file, naming: `01-topic-name.md`
- Clear writing: 8th-grade reading level, technical terms explained on first use

## Non-Functional (RAG System)
- High accuracy vector search: >=90% relevance for in-scope questions
- Fast lookup: p95 latency <2s for vector search
- Stable ingestion process: 99% success rate, automatic retry on transient failures
```

### 2.2 Chatbot Widget Underspecification (TO FIX)
**Location:** spec.md lines 88-90, plan.md lines 176-203

**Current (Vague):**
```
- **Chatbot widget embedded**
```

**Fix To Apply to spec.md section 4.1:**
```
3. Each chapter MUST have:
   - **Personalize for Me** button
   - **Translate to Urdu** button
   - **Chatbot widget embedded**: React component using Docusaurus theme,
     right-side floating button, expandable chat interface, sends POST to `/api/ask`,
     displays formatted markdown responses
```

### 2.3 CLI Ingestion Script Requirements (TO FIX)
**Location:** spec.md lines 124-128

**Current (Incomplete):**
```
7. MUST include a CLI ingestion script that:
   - Reads MD files
   - Splits them
   - Generates embeddings
   - Pushes to Qdrant
```

**Fix To Apply:**
```
7. MUST include a CLI ingestion script (`scripts/ingest_book.py`) that:
   - Reads all MD files from `apps/book-ui/docs` recursively
   - Splits them into semantic chunks (500-1000 tokens with 100 token overlap)
   - Generates OpenAI embeddings with retry (3 attempts, exponential backoff)
   - Pushes to Qdrant with progress bar and error logging
   - Idempotent: re-running updates existing entries without duplication
   - Error handling: logs failures, continues processing other files
   - Exit codes: 0 (success), 1 (partial failure), 2 (complete failure)
```

### 2.4 Signup Validation Rules (TO FIX)
**Location:** spec.md lines 183-187

**Current (Incomplete):**
```
### Signup:
Collect:
- Software background
- Hardware background
- GPU access
- Learning style
```

**Fix To Apply:**
```
### Signup:
Collect and validate:
- Software background (required, 10-500 chars, free text)
- Hardware background (required, 10-500 chars, free text)
- GPU access (required, boolean)
- Learning style (required, enum: ["visual", "hands-on", "theoretical", "mixed"])
- Email (required, valid email format)
- Password (required, min 8 chars, must include: 1 uppercase, 1 lowercase, 1 number)
```

---

## 3. MEDIUM PRIORITY FIXES

### 3.1 Docusaurus Version Inconsistency (TO FIX)
**Locations:** spec.md line 79 vs tasks.md line 32

**Fix for spec.md:**
```
1. MUST use **Docusaurus** v2 or v3 (current stable).
```

**Fix for tasks.md T002:**
```
- [x] T002 Initialize Docusaurus v3 project in `apps/book-ui/` (verify with `docusaurus --version`)
```

### 3.2 Vercel Deployment Inconsistency (TO FIX)
**Locations:** spec.md line 96 vs plan.md line 97

**Fix (Clarify in both files):**
```
5. Book MUST deploy to **GitHub Pages** (primary).
   Optional: Vercel deployment configuration provided but not required for MVP.
```

### 3.3 Terminology Standardization (TO FIX)

**Throughout all files, replace:**
- "Neon" → "Neon Postgres" (except where "Neon" is part of URL/brand)
- "RAG path" → "RAG pipeline"
- "RAG system" → "RAG pipeline" (when referring to the flow, keep "RAG System" for subsystem name)

### 3.4 Alembic Migration Task Missing (TO FIX)
**Location:** plan.md mentions Alembic (line 410), no task exists

**Add to tasks.md Phase 2 or Phase 5:**
```
- [ ] T021a [US3] Setup Alembic for database migrations in `apps/backend/` and create initial migration for user schema
```

### 3.5 Observability Tasks Missing (TO FIX)
**Location:** plan.md lines 426-443 detailed logging/metrics, no tasks

**Add to tasks.md Phase 8:**
```
- [ ] T040a [P] Setup structured logging with loguru in `apps/backend/logging_config.py`
- [ ] T040b [P] Implement Prometheus metrics endpoint `/metrics` for FastAPI
- [ ] T040c [P] Create basic Grafana dashboard configuration for backend monitoring
```

---

## 4. LOW PRIORITY FIXES

### 4.1 Duplicate Requirements (TO FIX)
**Location:** spec.md lines 54-59 duplicate lines 245-252

**Fix:** Remove duplication in section 3 (Global Requirements), keep only in section 5 (Acceptance Criteria)

---

## 5. LATENCY & DEGRADATION SPECS (TO ADD)

### 5.1 Add to plan.md NFR section (after line 320):
```
**Degradation Behavior When Targets Exceeded:**
- If p95 latency for RAG exceeds 10s: Return timeout message to user after 15s
- If OpenAI rate limit hit: Queue request with exponential backoff (max 3 retries)
- If Qdrant unavailable: Return specific error "RAG service temporarily unavailable"
- Book UI remains static and unaffected by backend issues
```

---

## Summary of Fixes

- **CRITICAL:** 1 Fixed (Constitution), 1 Pending (Security Tasks)
- **HIGH:** 0 Fixed, 4 Pending (NFRs, Chatbot, CLI, Signup)
- **MEDIUM:** 0 Fixed, 5 Pending (Version, Vercel, Terminology, Alembic, Observability)
- **LOW:** 0 Fixed, 1 Pending (Duplicates)

**Next Action:** Apply all pending fixes to spec.md, plan.md, and tasks.md

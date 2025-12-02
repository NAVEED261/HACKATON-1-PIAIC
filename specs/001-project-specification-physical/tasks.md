


# Tasks: Physical AI & Humanoid Robotics Textbook + RAG-Based Knowledge System

**Input**: Design documents from `/specs/001-project-specification-physical/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The specification does not explicitly request test tasks to be generated, so they are omitted from this list.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/` (as defined in plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create monorepo base directory and initial app folders `apps/book-ui`, `apps/backend`, `scripts/`
- [ ] T002 Initialize Docusaurus v2 project in `apps/book-ui/`
- [ ] T003 Initialize FastAPI project in `apps/backend/` with basic structure
- [ ] T004 [P] Configure initial Git repository and `.gitignore`
- [ ] T005 [P] Setup basic linting and formatting tools for Python (Black, Flake8) and JavaScript (ESLint, Prettier)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Configure environment variables (`.env` template) for OpenAI API keys and Neon Postgres connection string in `apps/backend/.env.template`
- [ ] T007 Implement basic error handling and logging configuration in `apps/backend/main.py`
- [ ] T008 Setup Dockerfile and docker-compose.yml for the FastAPI backend in `apps/backend/`

---

## Phase 3: User Story 1 - Book System Core Functionality & Deployment (Priority: P1) 🎯 MVP

**Goal**: Users can view the Physical AI & Humanoid Robotics textbook with standard navigation and search, deployed publicly.

**Independent Test**: Access the deployed book UI via its public URL and verify navigation, search, and content display.

### Implementation for User Story 1

- [ ] T009 [P] [US1] Structure Docusaurus content with course outline (ROS 2, Gazebo & Unity, NVIDIA Isaac, Humanoid Robotics, VLA, 13-week study plan) in `apps/book-ui/docs/`
- [ ] T010 [P] [US1] Configure Docusaurus sidebar navigation in `apps/book-ui/docusaurus.config.js`
- [ ] T011 [P] [US1] Configure Docusaurus navbar, search, and footer in `apps/book-ui/docusaurus.config.js`
- [ ] T012 [US1] Implement GitHub Pages deployment for Docusaurus book in `.github/workflows/deploy-book.yml`
- [ ] T013 [P] [US1] Add optional Vercel deployment preset for Docusaurus in `apps/book-ui/`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - RAG Chatbot Integration & Ingestion (Priority: P1)

**Goal**: Users can ask questions about the textbook content via an embedded chatbot and receive accurate, textbook-only answers.

**Independent Test**: Interact with the chatbot on a chapter page, ask a textbook-related question, verify accurate answer with source, and verify rejection for out-of-scope questions.

### Implementation for User Story 2

- [ ] T014 [US2] Create CLI ingestion script (reads MD, chunks, embeds, pushes to Qdrant) in `scripts/ingest_book.py`
- [ ] T015 [US2] Implement text chunking logic for Markdown files in `scripts/ingest_book.py`
- [ ] T016 [P] [US2] Implement OpenAI embeddings generation in `apps/backend/services/rag.py`
- [ ] T017 [P] [US2] Implement Qdrant client and storage logic (embeddings, metadata, chunk text) in `apps/backend/services/rag.py`
- [ ] T018 [US2] Implement RAG pipeline with OpenAI LLM for answers (textbook only, reject unrelated) in `apps/backend/services/rag.py`
- [ ] T019 [US2] Create `/ask` endpoint logic in `apps/backend/api/routers/ask.py` for RAG path
- [ ] T020 [US2] Embed chatbot widget in Docusaurus chapters, sending POST requests to `/api/ask` in `apps/book-ui/src/components/ChatbotWidget.js` (example path)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - User Authentication & Profile (Priority: P1)

**Goal**: Users can sign up, sign in, and manage their basic profile information.

**Independent Test**: Successfully create a new user, log in, view/update profile, and log out.

### Implementation for User Story 3

- [ ] T021 [US3] Implement Neon Postgres database connection and user data schema (users, hashed passwords, learning preferences, hardware/software background)
- [ ] T022 [US3] Implement `/auth/signup` API endpoint using Better-Auth in `apps/backend/services/auth.py` and `apps/backend/api/routers/auth.py`
- [ ] T023 [US3] Implement `/auth/signin` API endpoint using Better-Auth in `apps/backend/services/auth.py` and `apps/backend/api/routers/auth.py`
- [ ] T024 [US3] Implement `/user/profile` API endpoint (GET and PUT) for user profile management in `apps/backend/services/auth.py` and `apps/backend/api/routers/user.py`
- [ ] T025 [P] [US3] Integrate JWT-based authentication middleware in `apps/backend/main.py` or `apps/backend/middleware/auth.py`
- [ ] T026 [P] [US3] Implement client-side UI for signup, signin, and profile management in `apps/book-ui/src/components/AuthForms.js` (example path)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Chapter Personalization (Priority: P2)

**Goal**: Authenticated users can personalize chapter difficulty based on their profile.

**Independent Test**: Logged-in user personalizes a chapter, and the content is rewritten with adjusted difficulty.

### Implementation for User Story 4

- [ ] T027 [US4] Implement logic to modify chapter difficulty based on user profile in `apps/backend/services/personalization.py`
- [ ] T028 [US4] Implement OpenAI LLM call for rewriting chapter content based on personalization in `apps/backend/services/personalization.py`
- [ ] T029 [US4] Create `/chapter/personalize` API endpoint in `apps/backend/api/routers/chapter.py`
- [ ] T030 [US4] Integrate "Personalize for Me" button in Docusaurus chapters to call `/api/chapter/personalize` in `apps/book-ui/src/components/ChapterActions.js` (example path)

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - Urdu Chapter Translation (Priority: P2)

**Goal**: Authenticated users can translate chapter content to Urdu.

**Independent Test**: Logged-in user requests Urdu translation for a chapter, and the content is displayed in Urdu with preserved formatting.

### Implementation for User Story 5

- [ ] T031 [US5] Implement OpenAI LLM call for translating Markdown to Urdu in `apps/backend/services/translation.py`
- [ ] T032 [US5] Implement logic to preserve Markdown formatting during translation in `apps/backend/services/translation.py`
- [ ] T033 [US5] Create `/chapter/translate` API endpoint in `apps/backend/api/routers/chapter.py`
- [ ] T034 [US5] Integrate "Translate to Urdu" button in Docusaurus chapters to call `/api/chapter/translate` in `apps/book-ui/src/components/ChapterActions.js` (example path)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T035 Review and update `CLAUDE.md` and `constitution.md` based on implementation insights
- [ ] T036 Code cleanup and refactoring across subsystems
- [ ] T037 Performance optimization (e.g., caching RAG queries or personalized content)
- [ ] T038 Security hardening (e.g., input validation, dependency updates)
- [ ] T039 Generate public UI URL and public Backend URL after deployment
- [ ] T040 Final review of all Spec-Kit Plus files (`spec.md`, `plan.md`, `tasks.md`, `implementation docs`, ADRs, PHRs) for completeness and accuracy.

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
-   **User Stories (Phase 3-7)**: All depend on Foundational phase completion
    *   User stories can then proceed in parallel (if staffed)
    *   Or sequentially in priority order (P1 → P2)
-   **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

-   **User Story 1 (P1 - Book System)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
-   **User Story 2 (P1 - RAG Chatbot)**: Can start after Foundational (Phase 2) - Depends on Book System content for ingestion.
-   **User Story 3 (P1 - User Auth)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
-   **User Story 4 (P2 - Personalization)**: Can start after Foundational (Phase 2) - Depends on User Auth (US3) for user profiles and Book System (US1) for content.
-   **User Story 5 (P2 - Translation)**: Can start after Foundational (Phase 2) - Depends on User Auth (US3) for authenticated users and Book System (US1) for content.

### Within Each User Story

-   Models/Entities before services.
-   Services before API endpoints/UI integration.
-   Core implementation before cross-cutting concerns within the story.

### Parallel Opportunities

-   All tasks marked `[P]` within a phase can run in parallel (e.g., creating Docusaurus config files).
-   Once the Foundational phase completes, User Story 1, User Story 2, and User Story 3 can theoretically be started in parallel by different team members, though US2 depends on US1's content.
-   User Story 4 and User Story 5 can be started in parallel once their dependencies (US1, US3) are met.

---

## Parallel Example: User Story 1 (Book System Core Functionality & Deployment)

```bash
# Launch Docusaurus config tasks in parallel:
Task: "Configure Docusaurus sidebar navigation in apps/book-ui/docusaurus.config.js"
Task: "Configure Docusaurus navbar, search, and footer in apps/book-ui/docusaurus.config.js"
Task: "Add optional Vercel deployment preset for Docusaurus in apps/book-ui/"
```

---

## Implementation Strategy

### MVP First (User Story 1, 2, 3 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1 (Book System)
4.  Complete Phase 4: User Story 2 (RAG Chatbot)
5.  Complete Phase 5: User Story 3 (User Authentication)
6.  **STOP and VALIDATE**: Test User Stories 1, 2, and 3 independently and integrated.
7.  Deploy/demo if ready.

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready.
2.  Add User Story 1 (Book System) → Test independently → Deploy/Demo.
3.  Add User Story 2 (RAG Chatbot) → Test independently → Deploy/Demo.
4.  Add User Story 3 (User Authentication) → Test independently → Deploy/Demo.
5.  Add User Story 4 (Personalization) → Test independently → Deploy/Demo.
6.  Add User Story 5 (Translation) → Test independently → Deploy/Demo.
7.  Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    *   Developer A: User Story 1 (Book System)
    *   Developer B: User Story 3 (User Authentication)
    *   Developer C: User Story 2 (RAG Chatbot) - *can start after US1 provides content*
3.  Once US1 and US3 are done:
    *   Developer D: User Story 4 (Personalization)
    *   Developer E: User Story 5 (Translation)
4.  Stories complete and integrate independently.

---

## Notes

-   `[P]` tasks = different files, no dependencies
-   `[Story]` label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

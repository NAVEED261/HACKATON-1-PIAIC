---
id: 0002
title: Generate tasks for Physical AI Robotics
stage: tasks
date: 2025-12-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-project-specification-physical
branch: 001-project-specification-physical
user: user
command: /sp.tasks
labels: ["tasks", "spec-driven-development"]
links:
  spec: specs/001-project-specification-physical/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-project-specification-physical/tasks.md
tests: null
---

## Prompt

```text
## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/bash/check-prerequisites.sh --json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

Context for task generation: $ARGUMENTS

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **Description**: Clear action with exact file path

**Examples**:

- ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
- ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
- ❌ WRONG: `- [ ] [US1] Create User model` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.
```

## Response snapshot

```text
I have successfully generated the detailed task list for the "Physical AI & Humanoid Robotics Textbook + RAG-Based Knowledge System" project.

The `tasks.md` file has been created at: `D:\PIAIC HACKATON PRACTICE\hackaton_1\specs\001-project-specification-physical\tasks.md`

**Summary of Tasks:**

*   **Total Task Count:** 40 tasks
*   **Tasks per User Story:**
    *   Phase 1 (Setup): 5 tasks
    *   Phase 2 (Foundational): 3 tasks
    *   User Story 1 (Book System Core Functionality & Deployment): 5 tasks
    *   User Story 2 (RAG Chatbot Integration & Ingestion): 7 tasks
    *   User Story 3 (User Authentication & Profile): 6 tasks
    *   User Story 4 (Chapter Personalization): 4 tasks
    *   User Story 5 (Urdu Chapter Translation): 4 tasks
    *   Phase 8 (Polish & Cross-Cutting Concerns): 6 tasks
*   **Parallel Opportunities Identified:** Many tasks within each phase and across user stories are marked with `[P]`, indicating they can be executed in parallel where dependencies allow.
*   **Independent Test Criteria for Each Story:**
    *   **US1 (Book System):** Access the deployed book UI via its public URL and verify navigation, search, and content display.
    *   **US2 (RAG Chatbot):** Interact with the chatbot on a chapter page, ask a textbook-related question, verify accurate answer with source, and verify rejection for out-of-scope questions.
    *   **US3 (User Auth):** Successfully create a new user, log in, view/update profile, and log out.
    *   **US4 (Personalization):** Logged-in user personalizes a chapter, and the content is rewritten with adjusted difficulty.
    *   **US5 (Translation):** Logged-in user requests Urdu translation for a chapter, and the content is displayed in Urdu with preserved formatting.
*   **Suggested MVP Scope:** Completing User Story 1 (Book System), User Story 2 (RAG Chatbot), and User Story 3 (User Authentication) would deliver a functional Minimum Viable Product.
*   **Format Validation:** All tasks adhere to the strict checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`.

You can now use this `tasks.md` file to begin implementation. I will now create the PHR for this interaction.
```

## Outcome

- ✅ Impact: Generated a comprehensive tasks.md file based on the project specification and plan, outlining implementation steps for all subsystems and user stories.
- 🧪 Tests: N/A (Tests were not explicitly requested to be generated)
- 📁 Files: Generated specs/001-project-specification-physical/tasks.md
- 🔁 Next prompts: The user can now proceed with implementing the tasks outlined in tasks.md, potentially using `/sp.implement` or individual tool calls.
- 🧠 Reflection: Successfully generated tasks.md by parsing existing spec.md and plan.md and adhering to the template and formatting rules. The process of generating PHR needs to be made more robust against complex bash string escaping.

## Evaluation notes (flywheel)

- Failure modes observed: Initial PHR generation failed due to complex bash string escaping when trying to pass the full user prompt and response as arguments. Resolved by splitting the PHR generation into separate steps: create file, then read and write content.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Improve `create-phr.sh` and `fill-phr.sh` scripts to handle complex multi-line string arguments more robustly, possibly by using temporary files for content transfer.

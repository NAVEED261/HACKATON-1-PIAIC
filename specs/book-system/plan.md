### Implementation Plan for Book System (Docusaurus)

---

This plan outlines the architectural approach and implementation strategy for the Docusaurus Book System, adhering to the requirements in `specs/book-system/spec.md`.

### 1. Scope and Dependencies

**In Scope:**

*   A complete Docusaurus v2 textbook covering ROS 2, Gazebo & Unity, NVIDIA Isaac, Humanoid Robotics, VLA, and a 13-week study plan.
*   User interface elements including sidebar navigation, navbar, search functionality, and footer.
*   Integration of per-chapter buttons: "Personalize for Me", "Translate to Urdu", and an embedded chatbot widget.
*   Deployment to GitHub Pages as the primary target, with an optional Vercel deployment preset.

**External Dependencies:**

*   **Docusaurus v2:** The foundational frontend framework for developing and rendering the textbook user interface.
*   **GitHub Pages:** The primary hosting platform for the static Docusaurus book.
*   **Vercel:** An optional hosting service for deploying the Docusaurus book.

### 2. Key Decisions and Rationale

*   **Decision: Docusaurus v2 Framework**
    *   **Rationale:** Explicitly mandated by the specification, Docusaurus v2 is chosen for its excellent documentation features, Markdown-first approach, and ease of deployment for static sites.

### 3. Interfaces and API Contracts

*   **Chatbot Widget Interaction:**
    *   **Method:** `POST`
    *   **Endpoint:** `/api/ask` (on the FastAPI Orchestrator)
    *   **Request Body:** `application/json` with schema: `{"question": "string"}`.
*   **"Personalize for Me" Button Interaction:**
    *   **Method:** `POST`
    *   **Endpoint:** `/api/chapter/personalize` (on the FastAPI Orchestrator)
    *   **Request Body:** `application/json` with schema: `{"chapter_content": "string", "user_id": "string"}`.
*   **"Translate to Urdu" Button Interaction:**
    *   **Method:** `POST`
    *   **Endpoint:** `/api/chapter/translate` (on the FastAPI Orchestrator)
    *   **Request Body:** `application/json` with schema: `{"chapter_content": "string", "target_language": "string"}` (defaulting to "Urdu").

### 4. Non-Functional Requirements (NFRs) and Budgets

*   **Clean Markdown organization:** Adheres to CommonMark specification and a defined style guide. Verified through linting and review.
*   **Easy contribution structure:** Includes a `CONTRIBUTING.md` guide and clear documentation for adding new content. Verified by existence and clarity of documentation.
*   **Clear writing for beginners:** Content uses simple language, avoids jargon where possible, and provides explanations for technical terms. Verified through content review and user feedback.

### 5. Data Management and Migration

*   **Source of Truth:** The Markdown files residing in the `/apps/book-ui/docs` directory.
*   **Migration and Rollback:** Version control (Git) for Markdown files. Docusaurus deployments are static; therefore, rolling back to a previous version involves deploying an older Git commit.

### 6. Operational Readiness

*   **Deployment:** A dedicated GitHub Actions workflow will automate the build process and deployment to GitHub Pages.

### 7. Risk Analysis and Mitigation

*   **Risk:** Stale content due to lack of updates.
    *   **Mitigation:** Establish a regular review cycle for textbook content and ensure clear contribution guidelines.

### 8. Evaluation and Validation

*   **Definition of Done:** Docusaurus book deploys publicly. Navigation, search, and content display are functional. All required Spec-Kit Plus files exist.
*   **Output Validation:** Public UI URL is accessible and correctly points to the deployed book.

### 9. Architectural Decision Record (ADR)

*   No new ADRs for the Book System at this stage.

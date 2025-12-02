# Quickstart Guide: Physical AI & Humanoid Robotics Textbook + RAG-Based Knowledge System

This guide provides a quick overview and essential steps to get the core components of the project up and running.

---

## 1. Project Structure Overview

The project is a monorepo with the following key directories:

*   `/apps/book-ui/`: Docusaurus frontend for the textbook.
*   `/apps/backend/`: FastAPI backend for RAG, Auth, and Personalization APIs.
*   `/scripts/`: Contains utility scripts, including the Qdrant ingestion script.
*   `/specs/001-project-specification-physical/`: This feature's specification, plan, data models, contracts, and research.

---

## 2. Prerequisites

Ensure you have the following installed:

*   **Python 3.12+**
*   **Node.js 20.x+**
*   **npm or yarn** (for Docusaurus)
*   **Docker** and **Docker Compose** (for backend services like Qdrant/Neon Postgres if not using cloud versions)
*   **Git**

---

## 3. Setup and Installation

### 3.1. Backend Setup (FastAPI, Qdrant, Neon Postgres)

1.  **Navigate to the backend directory**:
    ```bash
    cd apps/backend
    ```
2.  **Create a virtual environment and install Python dependencies**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate # On Windows, use `.venv\Scripts\activate`
    pip install -r requirements.txt # (Requires requirements.txt to be created later)
    ```
3.  **Database Configuration**:
    *   **Neon Postgres**: Set up a Neon Postgres database and obtain connection credentials.
    *   **Qdrant**: You can run Qdrant locally via Docker or use Qdrant Cloud.
        *   **Docker (local)**:
            ```bash
            docker run -p 6333:6333 -p 6334:6334 -d qdrant/qdrant
            ```
4.  **Environment Variables**: Create an `.env` file in `apps/backend/` based on an `.env.template` (to be created) with your database, Qdrant, and OpenAI API keys.

### 3.2. Frontend Setup (Docusaurus)

1.  **Navigate to the frontend directory**:
    ```bash
    cd apps/book-ui
    ```
2.  **Install Node.js dependencies**:
    ```bash
    npm install # or yarn install
    ```

---

## 4. Running the Applications

### 4.1. Run FastAPI Backend

1.  **Activate Python virtual environment**:
    ```bash
    cd apps/backend
    source .venv/bin/activate
    ```
2.  **Start the FastAPI server**:
    ```bash
    uvicorn main:app --reload # (Requires main.py to be created later)
    ```
    The backend will typically run on `http://127.0.0.1:8000`.

### 4.2. Run Docusaurus Frontend

1.  **Navigate to the frontend directory**:
    ```bash
    cd apps/book-ui
    ```
2.  **Start the Docusaurus development server**:
    ```bash
    npm run start # or yarn start
    ```
    The Docusaurus site will usually open in your browser at `http://localhost:3000`.

---

## 5. Ingesting Textbook Content into Qdrant

This step is crucial for the RAG system to function.

1.  **Ensure Qdrant is running** (local Docker or cloud instance).
2.  **Run the ingestion CLI script**:
    ```bash
    cd scripts
    python ingest_qdrant.py # (Script name is a placeholder, to be created)
    ```
    This script will read Markdown files from `/apps/book-ui/docs`, chunk them, generate OpenAI embeddings, and push them to your configured Qdrant instance.

---

## 6. Testing API Endpoints

Once both frontend and backend are running, you can:

*   Interact with the Docusaurus UI and the embedded chatbot.
*   Use tools like Postman, Insomnia, or `curl` to test the FastAPI endpoints (`/ask`, `/auth/*`, `/user/*`, `/chapter/*`).

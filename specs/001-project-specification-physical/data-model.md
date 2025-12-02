# Data Model for Physical AI & Humanoid Robotics Textbook + RAG-Based Knowledge System

This document defines the key entities, their fields, relationships, and validation rules for the project.

---

## 1. User Entity (Neon Postgres)

**Purpose**: Stores user authentication, profile, and personalization preferences.

**Fields**:
- `user_id` (Primary Key, UUID): Unique identifier for the user.
- `email` (String, Unique): User's email address.
- `password_hash` (String): Hashed password for secure authentication (using Better-Auth).
- `software_background` (String/Text): User's self-reported software experience (e.g., Python, JavaScript, ROS).
- `hardware_background` (String/Text): User's self-reported hardware experience (e.g., Raspberry Pi, Arduino, NVIDIA Jetson).
- `gpu_access` (Boolean): Indicates if the user has access to a GPU.
- `learning_style` (String/Enum): User's preferred learning style (e.g., Visual, Auditory, Kinesthetic, Reading/Writing).
- `created_at` (Timestamp): Timestamp of user creation.
- `updated_at` (Timestamp): Last update timestamp.

**Relationships**:
- One-to-many with `ChapterPersonalization` (implicit, for user-specific chapter rewrites).
- One-to-many with `ChapterTranslation` (implicit, for user-specific Urdu translations).

**Validation Rules**:
- `email` must be a valid email format and unique.
- `password_hash` must be securely stored (hashed).
- All fields required during signup (`software_background`, `hardware_background`, `gpu_access`, `learning_style`) must be present.

---

## 2. Chapter Content Chunks (Qdrant)

**Purpose**: Stores semantically chunked textbook content and its embeddings for the RAG system.

**Fields (stored as payload in Qdrant)**:
- `chunk_id` (UUID): Unique identifier for the content chunk.
- `chapter_id` (UUID/String): Identifier linking to the original chapter.
- `chapter_title` (String): Title of the chapter this chunk belongs to.
- `section_title` (String, Optional): Title of the section within the chapter.
- `content` (String): The text content of the chunk.
- `page_number` (Integer, Optional): Original page number from the textbook.
- `order_index` (Integer): Order of the chunk within the chapter/section.
- `embedding` (Vector): OpenAI embedding of the `content`.
- `created_at` (Timestamp): Timestamp of ingestion.

**Relationships**:
- Implicitly linked to the Book System's Docusaurus Markdown files.

**Validation Rules**:
- `chunk_id`, `chapter_id`, `chapter_title`, `content`, `order_index`, `embedding` are required.
- `embedding` must be a valid vector of the expected dimension from OpenAI.

---

## 3. Chapter Personalization / Translation Metadata (Neon Postgres)

**Purpose**: Stores metadata about personalized or translated chapters. This is distinct from the rewritten content, which would be dynamically generated or cached.

**Fields**:
- `record_id` (Primary Key, UUID): Unique identifier for this record.
- `user_id` (Foreign Key, UUID): Links to the `User` entity.
- `chapter_id` (UUID/String): Identifier for the chapter being personalized/translated.
- `action_type` (String/Enum): 'personalize' or 'translate'.
- `target_language` (String, Optional): e.g., 'Urdu' for translation.
- `difficulty_level` (String/Enum, Optional): e.g., 'Beginner', 'Intermediate', 'Advanced' for personalization.
- `generated_text_hash` (String, Optional): Hash of the generated content to check for caching/versioning (actual content not stored here due to potential size).
- `created_at` (Timestamp): Timestamp of the action.

**Relationships**:
- Many-to-one with `User`.

**Validation Rules**:
- `user_id`, `chapter_id`, `action_type` are required.
- `target_language` is required if `action_type` is 'translate'.
- `difficulty_level` is required if `action_type` is 'personalize'.

---

## 4. Book System (Docusaurus Structure - implicitly represented by files)

**Purpose**: The Docusaurus project serves as the static textbook content. Its structure is file-based rather than a traditional database model.

**Entities**:
- Markdown files: Each represents a chapter or section.
  - Frontmatter (YAML): `title`, `slug`, `sidebar_label`, `sidebar_position`, etc.
- Assets: Images, videos, etc.

**Relationships**:
- Structured hierarchy via Docusaurus routing.
- Referenced by `Chapter Content Chunks` in Qdrant.

**Validation Rules**:
- Adherence to Docusaurus file naming and frontmatter conventions.
- Valid Markdown syntax.

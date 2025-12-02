# API Contracts for Backend Orchestrator

This document defines the API endpoints, their inputs, outputs, and error handling for the FastAPI Backend Orchestrator.

---

## 1. `/ask` Endpoint

**Purpose**: Routes user questions to the appropriate RAG or SQL pipeline and returns an answer.

**Method**: `POST`

**URL**: `/ask`

**Request Body**:
```json
{
  "question": "string" // User's question
}
```

**Responses**:

*   **200 OK**:
    ```json
    {
      "answer": "string", // The generated answer from RAG or SQL
      "source": "RAG" | "SQL" // Indicates which pipeline provided the answer
    }
    ```
*   **400 Bad Request**:
    ```json
    {
      "detail": "string" // e.g., "Invalid question format"
    }
    ```
*   **404 Not Found**: (If a book-related question has no context)
    ```json
    {
      "detail": "I don't have enough context in the textbook to answer this."
    }
    ```
*   **500 Internal Server Error**:
    ```json
    {
      "detail": "string" // e.g., "An unexpected error occurred"
    }
    ```

---

## 2. Authentication APIs

### 2.1. `/auth/signup`

**Purpose**: Registers a new user with their profile information.

**Method**: `POST`

**URL**: `/auth/signup`

**Request Body**:
```json
{
  "email": "string",
  "password": "string", // Raw password, to be hashed by backend
  "software_background": "string",
  "hardware_background": "string",
  "gpu_access": "boolean",
  "learning_style": "string" // e.g., "Visual", "Auditory"
}
```

**Responses**:

*   **201 Created**:
    ```json
    {
      "message": "User registered successfully",
      "user_id": "uuid"
    }
    ```
*   **400 Bad Request**:
    ```json
    {
      "detail": "string" // e.g., "Email already registered", "Invalid input data"
    }
    ```
*   **500 Internal Server Error**:
    ```json
    {
      "detail": "string"
    }
    ```

### 2.2. `/auth/signin`

**Purpose**: Authenticates an existing user and provides an access token.

**Method**: `POST`

**URL**: `/auth/signin`

**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Responses**:

*   **200 OK**:
    ```json
    {
      "access_token": "string", // JWT or similar token
      "token_type": "bearer"
    }
    ```
*   **401 Unauthorized**:
    ```json
    {
      "detail": "Invalid credentials"
    }
    ```
*   **500 Internal Server Error**:
    ```json
    {
      "detail": "string"
    }
    ```

---

## 3. User APIs (Requires Authentication)

### 3.1. `/user/profile`

**Purpose**: Retrieves or updates the authenticated user's profile.

**Method**: `GET` / `PUT`

**URL**: `/user/profile`

**Authentication**: Bearer Token (JWT) in `Authorization` header.

**GET Response (200 OK)**:
```json
{
  "user_id": "uuid",
  "email": "string",
  "software_background": "string",
  "hardware_background": "string",
  "gpu_access": "boolean",
  "learning_style": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

**PUT Request Body**: (Partial updates allowed)
```json
{
  "software_background": "string", // Optional
  "hardware_background": "string", // Optional
  "gpu_access": "boolean",         // Optional
  "learning_style": "string"       // Optional
}
```

**PUT Response (200 OK)**:
```json
{
  "message": "Profile updated successfully",
  "user_id": "uuid"
}
```

**Common Errors (for GET/PUT)**:
*   **401 Unauthorized**: "Not authenticated"
*   **403 Forbidden**: "Not authorized"
*   **500 Internal Server Error**: "string"

### 3.2. `/chapter/personalize`

**Purpose**: Generates a personalized version of a specific chapter for the authenticated user.

**Method**: `POST`

**URL**: `/chapter/personalize`

**Authentication**: Bearer Token (JWT)

**Request Body**:
```json
{
  "chapter_id": "string", // Identifier for the chapter to personalize
  "target_difficulty": "string" // e.g., "Beginner", "Intermediate"
}
```

**Responses**:

*   **200 OK**:
    ```json
    {
      "personalized_content": "string", // The rewritten chapter content
      "message": "Chapter personalized successfully"
    }
    ```
*   **400 Bad Request**: "Invalid chapter ID or difficulty"
*   **401 Unauthorized**: "Not authenticated"
*   **500 Internal Server Error**: "string"

### 3.3. `/chapter/translate`

**Purpose**: Translates a specific chapter into Urdu for the authenticated user.

**Method**: `POST`

**URL**: `/chapter/translate`

**Authentication**: Bearer Token (JWT)

**Request Body**:
```json
{
  "chapter_id": "string" // Identifier for the chapter to translate
}
```

**Responses**:

*   **200 OK**:
    ```json
    {
      "translated_content": "string", // The Urdu translated chapter content
      "message": "Chapter translated successfully"
    }
    ```
*   **400 Bad Request**: "Invalid chapter ID"
*   **401 Unauthorized**: "Not authenticated"
*   **500 Internal Server Error**: "string"

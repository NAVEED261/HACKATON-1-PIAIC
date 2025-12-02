# Research Findings for Physical AI & Humanoid Robotics Textbook + RAG-Based Knowledge System

## 1. Language and Version Recommendations

*   **Decision**: Use Python 3.12 for FastAPI and related CLI scripts, and Node.js 20.x with TypeScript 5.1+ for Docusaurus.
*   **Rationale**: Python 3.12 offers significant performance improvements and is a stable, actively supported version for FastAPI in 2025. Node.js 20.x is the current Long-Term Support (LTS) version, providing stability and security, while TypeScript 5.1+ is the minimum required by Docusaurus and offers modern language features.
*   **Alternatives considered**:
    *   Python 3.10/3.11: Still supported but 3.12 offers better performance.
    *   Older Node.js versions: Not recommended due to EOL status and lack of security updates.

## 2. Testing Frameworks and Best Practices

### FastAPI (Python)

*   **Decision**: Implement testing using Pytest with `pytest-asyncio` for asynchronous tests, `httpx.AsyncClient` or FastAPI's `TestClient` for HTTP requests, and leverage dependency injection for mocking.
*   **Rationale**: Pytest is the industry standard for Python testing, offering flexibility and a rich ecosystem. `pytest-asyncio` is essential for handling FastAPI's asynchronous nature. `httpx` and `TestClient` provide efficient and reliable HTTP testing within the application. Dependency injection allows for effective mocking and isolation of units.
*   **Best Practices**: Test isolation, asynchronous testing, smart mocking, clean database testing (transactional rollbacks/in-memory DBs), CI/CD integration, comprehensive coverage (including error paths), structured test organization, utilizing dependency injection.

### Docusaurus (JavaScript/TypeScript)

*   **Decision**: Implement unit testing with Jest for components/utilities, E2E testing with Cypress or Selenium, and prioritize visual regression testing. Incorporate Docusaurus's broken link configurations and content linters.
*   **Rationale**: Jest is the go-to for React component unit testing. Cypress/Selenium provide robust E2E coverage for user flows. Visual regression testing is critical for a content-driven site to maintain UI consistency. Docusaurus's built-in tools and linters ensure content and link integrity.
*   **Best Practices**: Unit test components, comprehensive E2E testing, prioritize visual regression, content and link integrity (automated link checks, content linting), local development and testing (`docusaurus start`/`serve`), CI/CD integration, modular test architecture, data-driven testing.

## 3. Performance Goals

### RAG System (Qdrant + OpenAI)

*   **Decision**: Initial goals: Retrieval accuracy (Context Precision & Recall > 80%), Generation quality (Faithfulness & Answer Relevancy > 90%), Latency (< 2-3 seconds per query), Throughput (5-10 QPS).
*   **Rationale**: These are realistic starting points for a RAG system integrating Qdrant and OpenAI, balancing accuracy and responsiveness. Continuous monitoring and optimization will be key.
*   **Key Metrics**: Context Precision, Context Recall, Context Relevancy, Precision@k, Recall@k, Faithfulness/Groundedness, Answer Relevancy, Factual Correctness, Answer Semantic Similarity, Latency, Throughput, Cost per Query.

### FastAPI Backend

*   **Decision**: Initial goals: Raw Throughput (> 10,000 RPS for simple endpoints), Latency (< 100ms average for simple APIs, < 500ms for I/O-bound), Concurrency (handle hundreds to thousands).
*   **Rationale**: FastAPI's asynchronous nature supports high throughput. These goals are achievable with proper optimization and architectural considerations.
*   **Key Metrics**: Raw Throughput (RPS), Latency, Concurrency.

### Docusaurus Frontend

*   **Decision**: Initial goals (Core Web Vitals): LCP (< 2.5s), INP (< 200ms), CLS (< 0.1), Overall Page Load (< 2s).
*   **Rationale**: These align with current web performance standards and contribute to a good user experience for a documentation site.
*   **Key Metrics**: Largest Contentful Paint (LCP), Interaction to Next Paint (INP), Cumulative Layout Shift (CLS), Page Load Time.

## 4. Operational and Security Constraints

*   **Decision**: Implement robust dependency management, comprehensive CI/CD, secure handling of secrets, data encryption, strong access controls, content moderation for AI, API rate limiting, and extensive observability. Address Docusaurus plugin vulnerabilities.
*   **Rationale**: These are critical to ensure the stability, security, and maintainability of a monorepo web application with multiple integrated services and sensitive data. Early consideration of these constraints mitigates future risks.
*   **Key Constraints**:
    *   **Deployment**: Dependency alignment in monorepo, CI/CD for multiple services, Docusaurus `docusaurus-plugin-content-gists` vulnerability (CVE-2025-53624, update to 4.0.0+), secure deployment keys/secrets.
    *   **Data Handling**: Qdrant (encryption at rest/in transit, RBAC, API keys, isolation, config optimization, compression), Neon Postgres (SSL/TLS, strong passwords, proxy, IP allowlist, protected branches, multi-tenancy/isolation, data anonymization, separation of compute/storage), OpenAI (data privacy, content moderation, constraining user input, usage policies).
    *   **API Limits**: OpenAI rate limiting, limiting output tokens.
    *   **General**: API key safety (no hardcoding, rotation), observability (Qdrant with OpenMetrics), load testing, human oversight (for OpenAI outputs), user authentication/identification (KYC), robust data access controls.

## 5. Scale and Scope Estimates

*   **Decision**: Initial user base 500-2,000 monthly for textbook, 1,000-5,000 monthly chatbot interactions. Content volume: 300-500 A5 pages for textbook (500MB-1GB build), RAG knowledge base starting with full textbook and scaling to 5,000-20,000 knowledge chunks.
*   **Rationale**: These estimates provide a baseline for resource planning and architecture design, allowing for growth as the project matures.
*   **Considerations**: Docusaurus can handle large content volumes. The RAG chatbot market is growing rapidly, indicating potential for significant interaction.

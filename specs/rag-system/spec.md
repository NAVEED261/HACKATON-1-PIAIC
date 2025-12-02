# 🤖 4.2 RAG System Specification

## Purpose
Define WHAT the RAG pipeline must do.

## Functional Requirements

1. MUST index all Markdown files in `/apps/book-ui/docs`.
2. MUST chunk chapters into semantic units.
3. MUST embed using **OpenAI embeddings**.
4. MUST store:
   - Embeddings
   - Metadata
   - Chunk text
   in **Qdrant**.
5. RAG MUST use **OpenAI LLM** for final answers.
6. RAG MUST:
   - Use only textbook vectors
   - Reject unrelated questions
7. MUST include a CLI ingestion script that:
   - Reads MD files
   - Splits them
   - Generates embeddings
   - Pushes to Qdrant

## Non-Functional
- High accuracy vector search: Achieves >90% recall for relevant textbook content queries.
- Fast lookup: p95 latency for vector search queries is <200ms.
- Stable ingestion process: Ingestion script has a success rate of >99% and handles malformed Markdown gracefully.

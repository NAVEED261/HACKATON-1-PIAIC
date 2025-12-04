#!/usr/bin/env python3
"""
RAG Ingestion Script - Physical AI & Humanoid Robotics Textbook
Complete implementation with OpenAI embeddings and Qdrant storage
"""

import os
import sys
import time
import hashlib
import re
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend directory
backend_env = Path(__file__).parent.parent / "apps" / "backend" / ".env"
load_dotenv(backend_env)

try:
    from openai import OpenAI
    from qdrant_client import QdrantClient, models
except ImportError as e:
    print(f"❌ Missing packages. Run: pip install openai qdrant-client python-dotenv")
    sys.exit(2)

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_HOST", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

COLLECTION_NAME = "book_chunks"
EMBEDDING_MODEL = "text-embedding-ada-002"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

def chunk_markdown(content: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    """Smart markdown chunking with overlap"""
    sections = re.split(r'\n\n+', content)
    chunks = []
    current_chunk = []
    current_length = 0

    for section in sections:
        section_length = len(section.split())
        if current_length + section_length <= chunk_size:
            current_chunk.append(section)
            current_length += section_length
        else:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
            current_chunk = [section]
            current_length = section_length

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    # Add overlap
    final_chunks = []
    for i, chunk in enumerate(chunks):
        if i > 0 and overlap > 0:
            prev_words = chunks[i-1].split()
            overlap_text = " ".join(prev_words[-overlap:])
            final_chunks.append(overlap_text + "\n\n" + chunk)
        else:
            final_chunks.append(chunk)

    return final_chunks

def generate_embedding_with_retry(text: str, max_retries: int = 3):
    """Generate embedding with exponential backoff"""
    for attempt in range(max_retries):
        try:
            response = openai_client.embeddings.create(input=[text], model=EMBEDDING_MODEL)
            return response.data[0].embedding
        except Exception as e:
            wait_time = 2 ** attempt
            print(f"  ⚠ Retry {attempt + 1}/{max_retries}: {e}")
            if attempt < max_retries - 1:
                time.sleep(wait_time)
            else:
                return []
    return []

def create_collection_if_not_exists():
    """Create Qdrant collection"""
    try:
        collections = [c.name for c in qdrant_client.get_collections().collections]
        if COLLECTION_NAME not in collections:
            print(f"📦 Creating collection: {COLLECTION_NAME}")
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
            )
        else:
            print(f"✅ Collection exists: {COLLECTION_NAME}")
    except Exception as e:
        print(f"❌ Collection error: {e}")
        sys.exit(2)

def generate_chunk_id(file_path: str, chunk_index: int):
    """Generate deterministic ID for idempotency"""
    return hashlib.md5(f"{file_path}:{chunk_index}".encode()).hexdigest()

def ingest_file(file_path: Path, docs_path: Path):
    """Ingest single file with embeddings"""
    try:
        content = file_path.read_text(encoding='utf-8')
        if not content.strip():
            return (0, 0)

        chunks = chunk_markdown(content)
        print(f"  📄 {len(chunks)} chunks")

        points = []
        for i, chunk in enumerate(chunks):
            embedding = generate_embedding_with_retry(chunk)
            if not embedding:
                continue

            chunk_id = generate_chunk_id(str(file_path), i)
            points.append(models.PointStruct(
                id=chunk_id,
                vector=embedding,
                payload={
                    "chunk_text": chunk,
                    "file_path": str(file_path.relative_to(docs_path)),
                    "chunk_index": i
                }
            ))

        if points:
            qdrant_client.upsert(collection_name=COLLECTION_NAME, wait=True, points=points)
            print(f"  ✅ Uploaded {len(points)} chunks")
            return (len(points), 0)

        return (0, len(chunks))
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return (0, 1)

def main():
    print("=" * 60)
    print("🚀 RAG Ingestion - Physical AI & Humanoid Robotics")
    print("=" * 60)

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        sys.exit(2)

    docs_path = Path(__file__).parent.parent / "apps" / "book-ui" / "docs"
    if not docs_path.exists():
        print(f"❌ Docs not found: {docs_path}")
        sys.exit(2)

    print(f"📁 Reading from: {docs_path}")
    create_collection_if_not_exists()

    md_files = list(docs_path.rglob("*.md")) + list(docs_path.rglob("*.mdx"))
    if not md_files:
        print("⚠ No markdown files found")
        sys.exit(1)

    print(f"\n📚 Found {len(md_files)} files")
    print("=" * 60)

    total_success, total_failure = 0, 0

    for idx, file_path in enumerate(md_files, 1):
        print(f"\n[{idx}/{len(md_files)}] {file_path.relative_to(docs_path)}")
        success, failure = ingest_file(file_path, docs_path)
        total_success += success
        total_failure += failure

    print("\n" + "=" * 60)
    print(f"✅ Success: {total_success} chunks")
    print(f"❌ Failed: {total_failure} chunks")
    print(f"📁 Files: {len(md_files)}")

    sys.exit(0 if total_failure == 0 else (1 if total_success > 0 else 2))

if __name__ == "__main__":
    main()

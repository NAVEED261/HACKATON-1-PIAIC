import os
from openai import OpenAI
from qdrant_client import QdrantClient, models

# Initialize OpenAI client (API key will be read from OPENAI_API_KEY environment variable)
openai_client = OpenAI()

# Initialize Qdrant client
qdrant_client = QdrantClient(
    host=os.getenv("QDRANT_HOST"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

COLLECTION_NAME = "book_chunks"

def get_openai_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    """
    Generates OpenAI embeddings for a given text.
    """
    try:
        response = openai_client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

def upsert_vectors_to_qdrant(chunks: list[str], embeddings: list[list[float]], metadatas: list[dict]):
    """
    Upserts (inserts or updates) vectors and their payloads to Qdrant.
    """
    points = []
    for i, (chunk, embedding, metadata) in enumerate(zip(chunks, embeddings, metadatas)):
        points.append(
            models.PointStruct(
                id=i,  # Simple incremental ID for now
                vector=embedding,
                payload={
                    "chunk_text": chunk,
                    **metadata
                }
            )
        )

    try:
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            wait=True,
            points=points
        )
        print(f"Successfully upserted {len(points)} points to Qdrant.")
    except Exception as e:
        print(f"Error upserting points to Qdrant: {e}")

def search_qdrant(query_embedding: list[float], limit: int = 3) -> list[str]:
    """
    Searches Qdrant for the most relevant document chunks.
    """
    try:
        search_result = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=limit,
            append_payload=True,
        )
        return [hit.payload["chunk_text"] for hit in search_result if hit.payload and "chunk_text" in hit.payload]
    except Exception as e:
        print(f"Error searching Qdrant: {e}")
        return []

def get_rag_answer(question: str) -> str:
    """
    Implements the RAG pipeline to get an answer from the textbook content.
    """
    query_embedding = get_openai_embedding(question)
    if not query_embedding:
        return "Error: Could not generate embedding for the question."

    relevant_chunks = search_qdrant(query_embedding)

    if not relevant_chunks:
        return "I'm sorry, I couldn't find relevant information in the textbook to answer your question. Please try rephrasing or ask a question directly related to the Physical AI & Humanoid Robotics textbook content."

    context = "\n\n".join(relevant_chunks)

    prompt = f"""You are an AI assistant specialized in Physical AI & Humanoid Robotics. Answer the user's question based ONLY on the provided textbook context. If the answer is not in the context, state that you cannot answer from the textbook and, if appropriate, suggest that the question might be outside the scope of the textbook. Do not use any outside knowledge.

Textbook Context:
{context}

User Question: {question}

Answer:"""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or a more capable model like gpt-4
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating LLM response: {e}")
        return "An error occurred while generating the answer."

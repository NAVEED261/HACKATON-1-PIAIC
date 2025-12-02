import argparse
import os
import re

def chunk_markdown(filepath: str, chunk_size: int = 1000, overlap: int = 200):
    """
    Reads a Markdown file, splits it into chunks, and returns them.
    A simple chunking strategy: splits by double newlines, then merges chunks
    to meet a target chunk size.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by double newlines to get initial sections (e.g., paragraphs, code blocks)
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

    # Simple overlap (could be improved for more semantic splitting)
    final_chunks = []
    for i, chunk in enumerate(chunks):
        if i > 0 and overlap > 0:
            # Add a bit of the previous chunk for context
            prev_chunk_words = chunks[i-1].split()
            overlap_text = " ".join(prev_chunk_words[-overlap:])
            final_chunks.append(overlap_text + "\n\n" + chunk)
        else:
            final_chunks.append(chunk)

    return final_chunks

def main():
    parser = argparse.ArgumentParser(description="CLI tool to ingest Markdown book content into Qdrant for RAG.")
    parser.add_argument("docs_path", type=str, help="Path to the Docusaurus docs folder (e.g., apps/book-ui/docs)")
    args = parser.parse_args()

    if not os.path.isdir(args.docs_path):
        print(f"Error: Docs path '{args.docs_path}' is not a valid directory.")
        return

    print(f"Starting ingestion from: {args.docs_path}")

    for root, _, files in os.walk(args.docs_path):
        for file in files:
            if file.endswith(".md") or file.endswith(".mdx"):
                filepath = os.path.join(root, file)
                print(f"Processing {filepath}...")
                chunks = chunk_markdown(filepath)
                for i, chunk in enumerate(chunks):
                    print(f"--- Chunk {i+1} ---")
                    print(chunk[:200] + ('...' if len(chunk) > 200 else '')) # Print first 200 chars
                    print("\n")
    print("Ingestion complete.")

if __name__ == "__main__":
    main()

import os
import re

def load_documents(folder="documents"):
    docs = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append({"filename": filename, "text": text})
    print(f"Loaded {len(docs)} documents")
    return docs

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def ingest(folder="documents"):
    docs = load_documents(folder)
    all_chunks = []
    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "source": doc["filename"],
                "chunk_index": i
            })
    print(f"Total chunks: {len(all_chunks)}")
    # Print 5 sample chunks
    for i in [0, 1, 2, 3, 4]:
        print(f"\n--- Chunk {i} from {all_chunks[i]['source']} ---")
        print(all_chunks[i]['text'][:300])
    return all_chunks

if __name__ == "__main__":
    chunks = ingest()
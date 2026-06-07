import chromadb
from sentence_transformers import SentenceTransformer
from ingest import ingest

def embed_and_store():
    # Load chunks from ingest.py
    chunks = ingest()

    # Load embedding model
    print("\nLoading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Set up ChromaDB
    client = chromadb.Client()
    collection = client.create_collection("neu_coop")

    # Embed and store
    print("Embedding and storing chunks...")
    texts = [c["text"] for c in chunks]
    sources = [c["source"] for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    embeddings = model.encode(texts).tolist()

    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"source": s} for s in sources],
        ids=ids
    )

    print(f"Stored {len(texts)} chunks in ChromaDB")
    return collection, model

def retrieve(query, collection, model, top_k=5):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    return results

if __name__ == "__main__":
    collection, model = embed_and_store()

    # Test with 3 evaluation questions
    test_queries = [
        "What is the average co-op pay at Northeastern?",
        "Is co-op required at Northeastern?",
        "What mistakes do students make during their first co-op search?"
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"QUERY: {query}")
        results = retrieve(query, collection, model)
        for i, (doc, meta, distance) in enumerate(zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )):
            print(f"\n[{i+1}] Source: {meta['source']} | Distance: {distance:.3f}")
            print(doc[:200])
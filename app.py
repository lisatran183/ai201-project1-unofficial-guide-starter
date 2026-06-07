import os
import gradio as gr
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from ingest import ingest
from dotenv import load_dotenv

load_dotenv()

# Setup
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.create_collection("neu_coop")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Ingest and embed
chunks = ingest()
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
print("Ready!")

def ask(question):
    # Retrieve top 5 chunks
    query_embedding = model.encode([question]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=5)
    
    retrieved_chunks = results["documents"][0]
    retrieved_sources = [m["source"] for m in results["metadatas"][0]]
    
    # Build context
    context = "\n\n".join([
        f"[Source: {src}]\n{chunk}"
        for chunk, src in zip(retrieved_chunks, retrieved_sources)
    ])
    
    # Build prompt
    prompt = f"""You are a helpful assistant for Northeastern University students asking about co-op experiences.
Answer the question using ONLY the information provided in the documents below.
If the documents don't contain enough information to answer, say "I don't have enough information in my documents to answer that."
Always cite which document(s) your answer came from.

Documents:
{context}

Question: {question}

Answer:"""

    # Call Groq
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.choices[0].message.content
    sources_str = "\n".join(set(retrieved_sources))
    
    return answer, sources_str

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# NEU Co-op Unofficial Guide")
    gr.Markdown("Ask questions about Northeastern co-op experiences based on real student stories.")
    
    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    
    btn.click(ask, inputs=inp, outputs=[answer, sources])
    inp.submit(ask, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
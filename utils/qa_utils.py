import faiss
import numpy as np
from openai import OpenAI
from sentence_transformers import SentenceTransformer

client = OpenAI()
embedder = SentenceTransformer("all-MiniLM-L6-v2")  # lightweight, local embeddings

# Store chunks + embeddings for PDF Q&A
class PDF_QA:
    def __init__(self, text_chunks):
        self.chunks = text_chunks
        self.index = None
        self.embeddings = None
        self._build_index()

    def _build_index(self):
        """Build FAISS index from text chunks."""
        self.embeddings = embedder.encode(self.chunks, convert_to_numpy=True)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    def query(self, question, top_k=5):
        """Answer a question strictly using the PDF context."""
        # Encode query
        q_embedding = embedder.encode([question], convert_to_numpy=True)
        D, I = self.index.search(q_embedding, top_k)

        # Retrieve top-k chunks
        retrieved = [self.chunks[i] for i in I[0]]
        context = "\n\n".join(retrieved)

        # Strict prompt to prevent hallucination
        prompt = f"""
You are an assistant that ONLY answers using the provided context.
If the answer is not in the context, reply exactly with: "I cannot find the answer in the document."

Context:
{context}

Question: {question}
Answer:
"""

        # Query OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a strict PDF assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip(), context

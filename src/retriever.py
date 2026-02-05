import faiss
import pickle
import numpy as np
from src.embed_store import model

# Load FAISS index and chunks
try:
    index = faiss.read_index("db/faiss.index")
    chunks = pickle.load(open("db/chunks.pkl", "rb"))
    print("FAISS index and documents loaded successfully.")
except Exception as e:
    print("Error loading FAISS index:", e)
    index = None
    chunks = []

def retrieve(query, k=5):
    if index is None:
        return []

    # Encode query
    q_emb = model.encode([query], normalize_embeddings=True)

    # Search
    D, I = index.search(np.array(q_emb), k)

    # Return matched chunks
    results = [chunks[i] for i in I[0] if i < len(chunks)]
    return results

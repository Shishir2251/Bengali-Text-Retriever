import faiss
import pickle
import numpy as np
from src.embed_store import model

# ----------------------------
# Load FAISS index and chunks
# ----------------------------
try:
    index = faiss.read_index("db/faiss.index")
    chunks = pickle.load(open("db/chunks.pkl", "rb"))
    print("✅ FAISS index and chunks loaded successfully.")
except Exception as e:
    print("❌ Error loading FAISS index:", e)
    index = None
    chunks = []

# ----------------------------
# Retrieve relevant chunks
# ----------------------------
def retrieve(query, k=5):
    if index is None:
        return []

    # Encode query
    q_emb = model.encode([query], normalize_embeddings=True)
    q_emb = np.array(q_emb, dtype=np.float32)

    # Search FAISS
    D, I = index.search(q_emb, k)

    # Filter valid chunks
    results = [chunks[i] for i in I[0] if i < len(chunks) and len(chunks[i]) > 20]
    return results

# Example usage
if __name__ == "__main__":
    q = "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?"
    res = retrieve(q)
    for i, r in enumerate(res, 1):
        print(f"{i}. {r}\n")

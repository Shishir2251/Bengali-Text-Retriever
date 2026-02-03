import faiss, pickle
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")

index = faiss.read_index("db/faiss.index")
chunks = pickle.load(open("db/chunks.pkl", "rb"))

def retrieve(query, k=5):
    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), k)
    return [chunks[i] for i in I[0]]

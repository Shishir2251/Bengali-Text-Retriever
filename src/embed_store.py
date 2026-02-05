from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load HuggingFace model (BAAI/bge-m3)
model = SentenceTransformer("BAAI/bge-m3")

# --- Bangla-aware chunking ---
def chunk_text(text, chunk_size=6):
    """
    Splits text into chunks of 'chunk_size' sentences using Bengali full stop '।'
    """
    sentences = text.replace("\n", " ").split("।")
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = "। ".join(sentences[i:i+chunk_size]) + "।"
        chunks.append(chunk)
    return chunks

# --- Build FAISS vector DB from chunks ---
def build_vector_db(chunks):
    embeddings = model.encode(chunks, normalize_embeddings=True)  # fix typo
    index = faiss.IndexFlatIP(embeddings.shape[1])  # use cosine similarity
    index.add(np.array(embeddings, dtype=np.float32))
    faiss.write_index(index, "db/faiss.index")
    pickle.dump(chunks, open("db/chunks.pkl", "wb"))
    print("✅ FAISS index and chunks saved successfully!")

# --- Convert single text into embedding ---
def get_embedding(text):
    emb = model.encode([text], normalize_embeddings=True)
    return np.array(emb, dtype=np.float32)

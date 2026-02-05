from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load HuggingFace model
model = SentenceTransformer("BAAI/bge-m3")

# Bangla-aware chunking (no NLTK)
def chunk_text(text, chunk_size=6):
    sentences = text.replace("\n", " ").split("।")
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = "। ".join(sentences[i:i+chunk_size]) + "।"
        chunks.append(chunk)
    return chunks

# Build FAISS vector DB from chunks
def build_vector_db(chunks):
    # Encode embeddings with normalization (for cosine similarity)
    embeddings = model.encode(chunks, normalize_embeddings=True)  # FIXED typo
    # Use cosine similarity (IP) instead of L2
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(np.array(embeddings, dtype=np.float32))
    # Save index and chunks
    faiss.write_index(index, "db/faiss.index")
    pickle.dump(chunks, open("db/chunks.pkl", "wb"))
    print("FAISS index and chunks saved successfully!")

# Convert single text into embedding (for query)
def get_embedding(text):
    """
    Convert a string into a normalized vector embedding.
    Returns a numpy array of shape (1, embedding_dim)
    """
    emb = model.encode([text], normalize_embeddings=True)  # normalize for cosine similarity
    return np.array(emb, dtype=np.float32)

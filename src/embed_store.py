from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
# Load HuggingFace model
model = SentenceTransformer("BAAI/bge-m3")

# Chunk text into sentences
def chunk_text(text, chunk_size=4):
    sentences = sent_tokenize(text)
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = " ".join(sentences[i:i+chunk_size])
        chunks.append(chunk)
    return chunks
def chunk_text(text, chunk_size=4):
    # split by Bengali full stop
    sentences = text.replace("\n", " ").split("।")  
    sentences = [s.strip() for s in sentences if s.strip()]
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = "। ".join(sentences[i:i+chunk_size]) + "।"
        chunks.append(chunk)
    return chunks

# Build FAISS vector DB from chunks
def build_vector_db(chunks):
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings, dtype=np.float32))
    faiss.write_index(index, "db/faiss.index")
    pickle.dump(chunks, open("db/chunks.pkl", "wb"))
    print("FAISS index and chunks saved successfully!")

# Convert single text into embedding
def get_embedding(text):
    """
    Convert a string into a vector embedding using the SentenceTransformer model.
    Returns a numpy array of shape (1, embedding_dim)
    """
    emb = model.encode([text])
    return np.array(emb, dtype=np.float32)

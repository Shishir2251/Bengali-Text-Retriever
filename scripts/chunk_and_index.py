from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

EXTRACTED_TEXT_PATH = "data/extracted_text.txt"
INDEX_PATH = "data/faiss_index.index"
CHUNKS_PATH = "data/chunks.pkl"

embedder = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')  # Good for Bangla; try 'BAAI/bge-m3' if low scores

def load_text(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,  # Smaller for precise answers
        chunk_overlap=50,
        separators=["\n\n", "।", "\n", "?", "!", ".", "—", ";", "(ক)"]  # Handle MCQs
    )
    return splitter.split_text(text)

def vectorize_and_index(chunks: list[str]):
    embeddings = embedder.encode(chunks)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)  # Normalize
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Cosine index
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Indexed {len(chunks)} chunks.")

if __name__ == "__main__":
    text = load_text(EXTRACTED_TEXT_PATH)
    chunks = chunk_text(text)
    vectorize_and_index(chunks)
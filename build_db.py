# build_db.py

from src.embed_store import chunk_text, build_vector_db

# 1️⃣ Read the cleaned OCR text
text = open("clean.txt", "r", encoding="utf-8").read()

# 2️⃣ Split into Bangla-aware chunks
chunks = chunk_text(text)

# 3️⃣ Build FAISS index from chunks
build_vector_db(chunks)

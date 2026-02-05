# build_db_from_pdf.py
from src.embed_store import chunk_text, build_vector_db
import PyPDF2
import os

pdf_path = "data/HSC26-Bangla1st-Paper.pdf"  

# Read PDF text
text = ""
with open(pdf_path, "rb") as f:
    reader = PyPDF2.PdfReader(f)
    for page in reader.pages:
        text += page.extract_text() + " "  # add a space between pages

# Chunk the text
chunks = chunk_text(text)

# Build FAISS index and save chunks
os.makedirs("db", exist_ok=True)
build_vector_db(chunks)

print("✅ FAISS index and chunks built from PDF!")

from pdfminer.high_level import extract_text
import unicodedata
import re

PDF_PATH = "data/HSC26-Bangla1st-Paper.pdf"
OUTPUT_PATH = "data/extracted_text.txt"

def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)  # Fix Bangla glyphs
    text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)  # Remove zero-width
    text = re.sub(r'\n+', '\n', text).strip()
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_pdf_text(pdf_path: str) -> str:
    return clean_text(extract_text(pdf_path))

if __name__ == "__main__":
    text = extract_pdf_text(PDF_PATH)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Extracted text saved. Length: {len(text)} chars. Sample: {text[:200]}")
from pypdf import PdfReader
from preprocess import clean_text

def load_pdf(path):
    reader = PdfReader(path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    return clean_text(full_text)

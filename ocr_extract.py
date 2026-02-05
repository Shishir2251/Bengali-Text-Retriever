from pdf2image import convert_from_path
import pytesseract
import os
import re

# 1️⃣ Set the full path to your installed tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 2️⃣ Set TESSDATA_PREFIX to point to your tessdata folder
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# 3️⃣ Set Poppler path (for PDF -> images)
POPPLER_PATH = r"C:\Users\Shishir\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

# 4️⃣ Convert PDF pages to images
images = convert_from_path(
    "data/HSC26-Bangla1st-Paper.pdf",
    poppler_path=POPPLER_PATH,
    dpi=300
)

# 5️⃣ OCR each image to get text
text = ""
for img in images:
    # Perform OCR with Bengali language
    text += pytesseract.image_to_string(img, lang="ben") + "\n"

# 6️⃣ Clean OCR text automatically
def clean_text(text):
    lines = text.split("\n")
    good = []
    for l in lines:
        l = l.strip()
        # Keep lines longer than 20 chars, ignore MCQ options, numbers, page headers
        if len(l) > 20 and "(ক)" not in l and not re.match(r'^\d+$', l) and not l.startswith("["):
            good.append(l)
    return "\n".join(good)

cleaned_text = clean_text(text)

# 7️⃣ Save cleaned text
with open("clean.txt", "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print("✅ OCR done. Clean text saved to clean.txt")

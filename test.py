from pdf2image import convert_from_path
import pytesseract
import os

# Point to your tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# Convert PDF pages to images
pdf_path = "data/HSC26-Bangla1st-Paper.pdf"  # your PDF path
images = convert_from_path(pdf_path)

text = ""

for img in images:
    text += pytesseract.image_to_string(img, lang="ben")  # Bengali OCR

# Save the extracted text
with open("clean.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("OCR done! Check clean.txt")

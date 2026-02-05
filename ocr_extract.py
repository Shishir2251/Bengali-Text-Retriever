from pdf2image import convert_from_path
import pytesseract
import os

# 1️⃣ Set the full path to your installed tesseract.exe
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"


# 2️⃣ Set poppler path (you already downloaded it)
POPPLER_PATH = r"C:\Users\Shishir\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

# 3️⃣ Convert PDF pages to images
images = convert_from_path(
    "data/HSC26-Bangla1st-Paper.pdf",
    poppler_path=POPPLER_PATH,
    dpi=300
)

# 4️⃣ OCR each image to get text
text = ""
for img in images:
    text += pytesseract.image_to_string(img, lang="ben")  # Bengali language pack

# 5️⃣ Save extracted text
with open("clean.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("✅ OCR done. Text saved to clean.txt")

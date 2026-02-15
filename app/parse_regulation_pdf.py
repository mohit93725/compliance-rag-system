import fitz  # PyMuPDF
import os

PDF_PATH = "data/regulations/RBI.PDF"
OUTPUT_PATH = "data/regulations/MD44_text_clean.txt"

doc = fitz.open(PDF_PATH)

text = ""

for page_number in range(len(doc)):
    page = doc[page_number]
    page_text = page.get_text("text")  # cleaner extraction
    text += page_text + "\n\n"
    print(f"Processed page {page_number + 1}/{len(doc)}")

doc.close()

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved cleaned text to:", OUTPUT_PATH)

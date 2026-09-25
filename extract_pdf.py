import fitz  # PyMuPDF
import os

pdf_path = r"C:\Users\DESKTOP\.gemini\antigravity-ide\brain\0c647258-75ad-4bc1-ad44-97da5a8d80f8\.user_uploaded\media_1790358545727.pdf"
output_dir = r"C:\Users\DESKTOP\.gemini\antigravity-ide\brain\0c647258-75ad-4bc1-ad44-97da5a8d80f8\scratch"

os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"Total pages: {doc.page_count}")

# Extract text from all pages
all_text = []
for i, page in enumerate(doc):
    text = page.get_text()
    all_text.append(f"\n{'='*80}\nPAGE {i+1}\n{'='*80}\n{text}")

# Write all text to a single file
output_file = os.path.join(output_dir, "pdf_full_text.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(all_text))

print(f"Full text extracted to: {output_file}")
print(f"Total chars: {sum(len(t) for t in all_text)}")

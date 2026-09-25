import json
import re

transcript_path = r"C:\Users\DESKTOP\.gemini\antigravity-ide\brain\0c647258-75ad-4bc1-ad44-97da5a8d80f8\.system_generated\logs\transcript.jsonl"

ocr_text = ""
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            if data.get("type") == "USER_INPUT":
                content = data.get("content", "")
                if "==Start of OCR for page 1==" in content:
                    ocr_text = content
                    if data.get("is_truncated"):
                        print("Warning: Content is truncated.")
                    break
        except Exception as e:
            pass

if ocr_text:
    print("Found OCR text! Length:", len(ocr_text))
    with open("ocr_dump.txt", "w", encoding="utf-8") as out:
        out.write(ocr_text)
else:
    print("OCR text not found.")

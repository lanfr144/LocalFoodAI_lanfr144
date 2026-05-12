import os
from pypdf import PdfReader

def extract_pdf(pdf_path, txt_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extracted {pdf_path} to {txt_path}")
    except Exception as e:
        print(f"Failed to read {pdf_path}: {e}")

extract_pdf(r"c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\Project.pdf", "project_text.txt")
extract_pdf(r"c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\Retro Planning.pdf", "retro_planning_text.txt")

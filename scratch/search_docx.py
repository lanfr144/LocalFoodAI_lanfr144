import os
import zipfile
import xml.etree.ElementTree as ET

def get_paragraphs(path):
    try:
        doc = zipfile.ZipFile(path)
        xml_content = doc.read('word/document.xml')
        root = ET.fromstring(xml_content)
        
        paragraphs = []
        for paragraph in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            texts = [node.text for node in paragraph.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
            if texts:
                paragraphs.append("".join(texts))
        return paragraphs
    except Exception as e:
        return [f"Error: {e}"]

if __name__ == "__main__":
    path = r"c:\Users\lanfr144\Documents\DOPRO1\Antigravity\description.docx"
    paragraphs = get_paragraphs(path)
    for p in paragraphs:
        for word in ["LocalFood", "git.btshub", "evegi144", "lanfr144", "Francois"]:
            if word.lower() in p.lower():
                print(f"Match for '{word}':\n  {p}\n")

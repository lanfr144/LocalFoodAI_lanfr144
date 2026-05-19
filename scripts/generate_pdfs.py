import os
import glob
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

def main():
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    md_files = glob.glob(os.path.join(docs_dir, '*.md'))
    
    if not md_files:
        print("No markdown files found in docs/")
        return
        
    for md_file in md_files:
        pdf_file = md_file.replace('.md', '.pdf')
        print(f"Converting {os.path.basename(md_file)} to PDF...")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        pdf = MarkdownPdf(toc_level=2)
        pdf.add_section(Section(md_content))
        pdf.save(pdf_file)
        print(f"Saved {os.path.basename(pdf_file)}")

if __name__ == "__main__":
    main()

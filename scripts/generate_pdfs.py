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
            
        import subprocess
        try:
            log_info = subprocess.check_output(['git', 'log', '-1', '--format=%H %an %ae %ad %cn %ce %cd %N  %s', '--date=format:%Y/%m/%d %H:%M:%S'], encoding='utf-8').strip()
            try:
                tag_info = subprocess.check_output(['git', 'describe', '--tags', '--always'], stderr=subprocess.DEVNULL, encoding='utf-8').strip()
            except Exception:
                tag_info = ""
            
            if tag_info:
                git_id = f"$Id$"
            else:
                git_id = f"$Id$"
        except Exception:
            git_id = "$Id$"
            
        md_content = md_content.replace('$Id$', git_id)
        
        try:
            pdf = MarkdownPdf(toc_level=2)
            pdf.add_section(Section(md_content))
            pdf.save(pdf_file)
            print(f"Saved {os.path.basename(pdf_file)}")
        except Exception as e:
            print(f"WARNING: Could not save {os.path.basename(pdf_file)}. File might be locked or open in a viewer. Error: {e}")

if __name__ == "__main__":
    main()

#ident "@(#)$Format:LocalFoodAI_lanfr144:generate_pdfs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import glob
import re
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section

def main():
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')
    md_files = glob.glob(os.path.join(docs_dir, '*.md'))
    
    if not md_files:
        print("No markdown files found in docs/")
        return
        
    # Use relative paths for fonts to ensure portability of PDF generation
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')).replace('\\', '/')
    
    user_css = """
    * {
        color: #1a1a1a !important;
    }
    body {
        font-family: 'Helvetica', 'Arial', sans-serif !important;
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    h1, h2, h3, h4, h5, h6, h1 *, h2 *, h3 *, h4 *, h5 *, h6 * {
        color: #000000 !important;
        margin-top: 18px !important;
        margin-bottom: 8px !important;
    }
    pre {
        background-color: #f8f9fa !important;
        border: 1px solid #e9ecef !important;
        padding: 2px !important;
        margin-top: 8px !important;
        margin-bottom: 16px !important;
        border-radius: 3px !important;
        font-family: 'Courier New', 'Courier', monospace !important;
        font-size: 10pt !important;
        white-space: pre-wrap !important;
        word-break: break-all !important;
    }
    pre code, pre * {
        font-family: 'Courier New', 'Courier', monospace !important;
        font-size: 10pt !important;
        color: #212529 !important;
        background-color: #f8f9fa !important;
        white-space: pre-wrap !important;
        word-break: break-all !important;
    }
    code {
        font-family: 'Courier New', 'Courier', monospace !important;
        font-size: 10pt !important;
        color: #b02a37 !important;
        background-color: #f8f9fa !important;
        padding: 2px 4px !important;
        border-radius: 3px !important;
        white-space: pre-wrap !important;
        word-break: break-all !important;
    }
    a, a * {
        color: #0d6efd !important;
    }
    blockquote, blockquote * {
        color: #555555 !important;
        border-left: 4px solid #ccc !important;
        padding-left: 10px !important;
    }
    table, tr, td, th, table * {
        color: #1a1a1a !important;
        border-color: #cccccc !important;
    }
    th {
        background-color: #f2f2f2 !important;
    }
    ul, li {
        list-style-type: disc !important;
    }
    """

    for md_file in md_files:
        pdf_file = md_file.replace('.md', '.pdf')
        print(f"Converting {os.path.basename(md_file)} to PDF...")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        import subprocess
        def sanitize_name(name):
            if not name:
                return "Francois Lange"
            name_lower = name.lower()
            if "fran" in name_lower or "lange" in name_lower or "lanfr" in name_lower:
                return "Francois Lange"
            return name

        def get_git_info_for_file(file_path):
            try:
                cmd = [
                    "git", "log", "-1",
                    "--date=format:%Y/%m/%d %H:%M:%S",
                    "--format=%an|%ae|%ad|%cn|%ce|%cd|%H|%D|%N",
                    "--", file_path
                ]
                out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip()
                if out:
                    parts = out.split('|')
                    if len(parts) == 9:
                        parts[0] = sanitize_name(parts[0])
                        parts[3] = sanitize_name(parts[3])
                        return parts
            except Exception:
                pass
            author_name = "Francois Lange"
            try:
                author_email = subprocess.check_output(["git", "config", "user.email"], stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip() or "lanfr144@school.lu"
            except Exception:
                author_email = "lanfr144@school.lu"
            from datetime import datetime
            now_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            return [author_name, author_email, now_str, author_name, author_email, now_str, "Not Committed Yet", "local", "none"]

        # Dynamic smudging of the Format placeholder for this specific file
        base_name = os.path.basename(md_file)
        info = get_git_info_for_file(md_file)
        replacement = f"$Format:LocalFoodAI_lanfr144:generate_pdfs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
        
        # Replace the raw format template if present
        pattern = r'\$Format:LocalFoodAI_lanfr144:generate_pdfs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$'
        md_content = re.sub(pattern, replacement, md_content)
        
        # Clean up absolute file:/// paths to relative paths
        md_content = re.sub(r'file:///.*?/docs/([a-zA-Z0-9_-]+)\.md', r'\1.pdf', md_content, flags=re.IGNORECASE)
        md_content = re.sub(r'file:///.*?/Food/([a-zA-Z0-9_.-]+)', r'../\1', md_content, flags=re.IGNORECASE)
        
        # Add <br/> after code blocks to force copy-paste blank line
        md_content = re.sub(r'(```[a-zA-Z0-9_-]*\n[\s\S]*?\n```)', r'\1\n<br/>', md_content)
        
        # Convert any relative markdown links in standard format [text](filename.md) or [text](./filename.md) to point to .pdf
        md_content = re.sub(r'\]\((?!http|https)([a-zA-Z0-9_./-]+)\.md(#[a-zA-Z0-9_-]+)?\)', r'](\1.pdf\2)', md_content, flags=re.IGNORECASE)

        try:
            pdf = MarkdownPdf(toc_level=2, optimize=True, plugins={"mermaid": {}})
            
            if base_name == 'project_report.md':
                print("Splitting project_report.md into Portrait/Landscape/Portrait sections...")
                parts = md_content.split('## 2. Project File Catalog & Documentation')
                if len(parts) == 2:
                    portrait_part1 = parts[0]
                    remaining = parts[1]
                    parts2 = remaining.split('## 3. Directory Structure Map')
                    if len(parts2) == 2:
                        landscape_part = '## 2. Project File Catalog & Documentation' + parts2[0]
                        portrait_part2 = '## 3. Directory Structure Map' + parts2[1]
                        
                        pdf.add_section(Section(portrait_part1, paper_size="A4", root=root_dir), user_css=user_css)
                        pdf.add_section(Section(landscape_part, paper_size="A4-L", root=root_dir), user_css=user_css)
                        pdf.add_section(Section(portrait_part2, paper_size="A4", root=root_dir), user_css=user_css)
                    else:
                        print("WARNING: Could not find Directory Structure Map heading. Defaulting to full portrait.")
                        pdf.add_section(Section(md_content, paper_size="A4", root=root_dir), user_css=user_css)
                else:
                    print("WARNING: Could not find Project File Catalog heading. Defaulting to full portrait.")
                    pdf.add_section(Section(md_content, paper_size="A4", root=root_dir), user_css=user_css)
            else:
                pdf.add_section(Section(md_content, paper_size="A4", root=root_dir), user_css=user_css)
                
            # Post-process compiled PDF to insert header and footer
            import fitz
            doc = pdf._make_doc()
            total_pages = len(doc)
            
            # Parse title from md_content
            title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
            if title_match:
                doc_title = title_match.group(1).strip()
                doc_title = re.sub(r'[*_`#]', '', doc_title).strip()
            else:
                doc_title = os.path.basename(pdf_file).replace('.pdf', '').replace('_', ' ')
            
            image_path = os.path.join(docs_dir, 'am.png')
            
            for page_idx in range(total_pages):
                page = doc[page_idx]
                width = page.rect.width
                height = page.rect.height
                
                # Header layout
                # Left: am.png picture (if exists)
                if os.path.exists(image_path):
                    image_rect = fitz.Rect(48, 12, 48 + 16, 12 + 16)
                    page.insert_image(image_rect, filename=image_path)
                
                # Middle: document title (centered)
                # Right: "DOPRO1"
                r_text = "DOPRO1"
                fontsize = 8
                fontname = "helv"
                
                m_width = fitz.get_text_length(doc_title, fontname=fontname, fontsize=fontsize)
                r_width = fitz.get_text_length(r_text, fontname=fontname, fontsize=fontsize)
                
                page.insert_text(
                    fitz.Point((width - m_width) / 2, 22),
                    doc_title,
                    fontname=fontname,
                    fontsize=fontsize,
                    color=(0.5, 0.5, 0.5)
                )
                
                page.insert_text(
                    fitz.Point(width - 48 - r_width, 22),
                    r_text,
                    fontname=fontname,
                    fontsize=fontsize,
                    color=(0.5, 0.5, 0.5)
                )
                
                # Footer layout
                # Left: "lanfr144"
                # Middle: "Page X of Y"
                l_footer = "lanfr144"
                footer_text = f"Page {page_idx + 1} of {total_pages}"
                f_width = fitz.get_text_length(footer_text, fontname=fontname, fontsize=fontsize)
                
                page.insert_text(
                    fitz.Point(48, height - 22),
                    l_footer,
                    fontname=fontname,
                    fontsize=fontsize,
                    color=(0.5, 0.5, 0.5)
                )
                
                page.insert_text(
                    fitz.Point((width - f_width) / 2, height - 22),
                    footer_text,
                    fontname=fontname,
                    fontsize=fontsize,
                    color=(0.5, 0.5, 0.5)
                )
                
            # Deflate, clean, garbage collect and linearize the document
            # to fix Acrobat encoding and save prompts
            doc.save(pdf_file, clean=True, garbage=3, deflate=True)
            doc.close()
            pdf.temp_files.clean()
            
            print(f"Saved {os.path.basename(pdf_file)}")
            
            # Copy to workspace root if applicable
            import shutil
            if base_name == 'project_report.md':
                dest = os.path.join(root_dir, 'Project.pdf')
                try:
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.copy2(pdf_file, dest)
                    print("Successfully updated root Project.pdf")
                except Exception as copy_err:
                    print(f"WARNING: Could not copy to root Project.pdf: {copy_err}")
            elif base_name == 'retro_planning.md':
                dest = os.path.join(root_dir, 'Retro Planning.pdf')
                try:
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.copy2(pdf_file, dest)
                    print("Successfully updated root Retro Planning.pdf")
                except Exception as copy_err:
                    print(f"WARNING: Could not copy to root Retro Planning.pdf: {copy_err}")
                    
        except Exception as e:
            print(f"WARNING: Could not save {os.path.basename(pdf_file)}. File might be locked or open in a viewer. Error: {e}")

if __name__ == "__main__":
    main()
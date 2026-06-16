#ident "@(#)$Format:LocalFoodAI_lanfr144:generate_pdfs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
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
        
    # Resolve dynamic absolute paths for downloaded TrueType fonts
    fonts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', 'fonts')).replace('\\', '/')
    regular_font = f"{fonts_dir}/Roboto-Regular.ttf"
    bold_font = f"{fonts_dir}/Roboto-Bold.ttf"
    mono_font = f"{fonts_dir}/RobotoMono-Regular.ttf"
    
    user_css = f"""
    @font-face {{
        font-family: 'Roboto';
        src: url('{regular_font}');
    }}
    @font-face {{
        font-family: 'Roboto';
        font-weight: bold;
        src: url('{bold_font}');
    }}
    @font-face {{
        font-family: 'RobotoMono';
        src: url('{mono_font}');
    }}
    * {{
        color: #1a1a1a !important;
    }}
    body {{
        font-family: 'Roboto', sans-serif;
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }}
    h1, h2, h3, h4, h5, h6, h1 *, h2 *, h3 *, h4 *, h5 *, h6 * {{
        color: #000000 !important;
    }}
    code, pre, code *, pre * {{
        font-family: 'RobotoMono', monospace !important;
        color: #b02a37 !important;
        background-color: #f8f9fa !important;
    }}
    a, a * {{
        color: #0d6efd !important;
    }}
    blockquote, blockquote * {{
        color: #555555 !important;
        border-left: 4px solid #ccc !important;
        padding-left: 10px !important;
    }}
    table, tr, td, th, table * {{
        color: #1a1a1a !important;
        border-color: #cccccc !important;
    }}
    th {{
        background-color: #f2f2f2 !important;
    }}
    """

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
            pdf = MarkdownPdf(toc_level=2, optimize=True)
            base_name = os.path.basename(md_file)
            
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
                        
                        pdf.add_section(Section(portrait_part1, paper_size="A4"), user_css=user_css)
                        pdf.add_section(Section(landscape_part, paper_size="A4-L"), user_css=user_css)
                        pdf.add_section(Section(portrait_part2, paper_size="A4"), user_css=user_css)
                    else:
                        print("WARNING: Could not find Directory Structure Map heading. Defaulting to full portrait.")
                        pdf.add_section(Section(md_content, paper_size="A4"), user_css=user_css)
                else:
                    print("WARNING: Could not find Project File Catalog heading. Defaulting to full portrait.")
                    pdf.add_section(Section(md_content, paper_size="A4"), user_css=user_css)
            else:
                pdf.add_section(Section(md_content, paper_size="A4"), user_css=user_css)
                
            pdf.save(pdf_file)
            print(f"Saved {os.path.basename(pdf_file)}")
            
            # Copy to workspace root if applicable
            import shutil
            root_dir = os.path.join(os.path.dirname(__file__), '..')
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
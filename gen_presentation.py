import markdown
import os

files_to_merge = ['AI_History/Client_Presentation.md', 'AI_History/status_report.md', 'AI_History/Retrospective.md']
merged_md = ''
for fName in files_to_merge:
    if os.path.exists(fName):
        with open(fName, 'r', encoding='utf-8') as f:
            merged_md += f.read() + '\n\n---\n\n'

html_content = markdown.markdown(merged_md, extensions=['tables'])

html_template = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Customer Presentation</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 2rem; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #2980b9; margin-top: 2rem; }}
        h3 {{ color: #16a085; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 2rem; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; color: #333; }}
        @media print {{
            body {{ padding: 0; max-width: 100%; }}
            hr {{ page-break-after: always; border: 0; }}
        }}
    </style>
</head>
<body>
    <div style="text-align:center; margin-bottom: 3rem;">
        <h1 style="border: none;">Clinical Food AI Platform</h1>
        <p><strong>Master Deliverable Overview</strong></p>
    </div>
    {html_content}
</body>
</html>
'''

with open('Final_Presentation.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
print('Generated HTML!')

import re

try:
    with open('docs/User_Guide.md', 'r', encoding='utf-8') as f:
        user_guide_content = f.read()
    user_guide_content = re.sub(r'^#ident [^\n]+\n', '', user_guide_content)
    if not user_guide_content.startswith('# $Id$'):
        user_guide_content = '# $Id$\n' + user_guide_content.lstrip('# ')
        
    with open('docs/Technical_Document.md', 'r', encoding='utf-8') as f:
        tech_doc_content = f.read()
    tech_doc_content = re.sub(r'^#ident [^\n]+\n', '', tech_doc_content)
    if not tech_doc_content.startswith('# $Id$'):
        tech_doc_content = '# $Id$\n' + tech_doc_content.lstrip('# ')

    # Escape backslashes for python string literal representation
    user_guide_content_escaped = user_guide_content.replace('\\', '\\\\')
    tech_doc_content_escaped = tech_doc_content.replace('\\', '\\\\')

    with open('generate_docs.py', 'r', encoding='utf-8') as f:
        gen_content = f.read()

    # 1. Update User_Guide.md in docs dict
    user_guide_pattern = r'("User_Guide\.md":\s*\"\"\"[\s\S]*?\"\"\",)'
    new_user_guide_block = f'"User_Guide.md": """{user_guide_content_escaped}""",\n'
    gen_content = re.sub(user_guide_pattern, new_user_guide_block, gen_content)

    # 2. Add Technical_Document.md to docs dict
    tech_doc_block = f'    "Technical_Document.md": """{tech_doc_content_escaped}""",\n'
    if '"Technical_Document.md"' not in gen_content:
        idx = gen_content.find('"User_Guide.md"')
        if idx != -1:
            end_idx = gen_content.find('""",', idx)
            if end_idx != -1:
                insert_pos = end_idx + 5
                gen_content = gen_content[:insert_pos] + '\n' + tech_doc_block + gen_content[insert_pos:]
    else:
        # Overwrite existing Technical_Document.md block if present
        tech_doc_pattern = r'("Technical_Document\.md":\s*\"\"\"[\s\S]*?\"\"\",)'
        gen_content = re.sub(tech_doc_pattern, tech_doc_block, gen_content)

    # 3. Replace llama3.2-vision:11b with llama3.2:3b in gen_content
    gen_content = gen_content.replace('llama3.2-vision:11b', 'llama3.2:3b')

    with open('generate_docs.py', 'w', encoding='utf-8') as f:
        f.write(gen_content)
    print("Successfully updated generate_docs.py with escaped content!")
except Exception as e:
    print(f"Error updating generate_docs.py: {e}")

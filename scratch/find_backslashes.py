with open('docs/Technical_Document.md', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f, 1):
        if '\\' in line:
            print(f"Line {idx}: {repr(line)}")

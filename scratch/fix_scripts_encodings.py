import os

scripts_dir = 'scripts'
for filename in os.listdir(scripts_dir):
    if filename.endswith('.py') or filename.endswith('.sh'):
        path = os.path.join(scripts_dir, filename)
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Clean up bad bytes
            content = content.replace('Fran\ufffdois', 'François')
            content = content.replace('Franois', 'François')
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed encoding for {filename}")
        except Exception as e:
            print(f"Error on {filename}: {e}")

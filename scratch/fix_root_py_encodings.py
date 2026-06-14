import os

for filename in os.listdir('.'):
    if filename.endswith('.py'):
        try:
            with open(filename, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Clean up bad bytes
            content = content.replace('Fran\ufffdois', 'François')
            content = content.replace('Franois', 'François')
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed encoding for root file: {filename}")
        except Exception as e:
            print(f"Error on {filename}: {e}")

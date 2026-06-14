import sys

app_path = 'app.py'
try:
    with open(app_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Replace the replacement characters with proper 'ç' or 'c'
    content = content.replace('Fran\ufffdois', 'François')
    content = content.replace('Franois', 'François')
    
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully corrected app.py encoding!")
except Exception as e:
    print(f"Error correcting file encoding: {e}")

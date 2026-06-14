import os
import zipfile

def create_delivery_zip():
    zip_name = "LocalFoodAI_lanfr144_Delivery_make_delivery.zip"
    exclude_dirs = {".git", ".venv", "__pycache__", "node_modules", ".vscode", ".agents", "backups", "logs"}
    exclude_files = {
        "LocalFoodAI_lanfr144_Delivery.zip",
        "Copie de secours de description.wbk",
        "~$scription.docx",
    }
    
    print(f"Creating clean delivery archive: {zip_name}...")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, allowZip64=True ) as zipf:
        for root, dirs, files in os.walk('.'):
            # Modify dirs in-place to exclude specified directories recursively
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file in exclude_files:
                    continue
                # Exclude lock files or temp files starting with ~$
                if file.startswith("~$") or file.endswith(".pyc") or file.endswith(".wbk"):
                    continue
                
                # Exclude large raw CSV datasets (they will be synced automatically during setup)
                filepath = os.path.join(root, file)
                if file.endswith(".csv") or os.path.getsize(filepath) > 10 * 1024 * 1024: # Exclude files > 10MB
                    print(f"Skipping large file: {filepath} ({os.path.getsize(filepath) / (1024*1024):.2f} MB)")
                    continue
                
                relative_path = os.path.relpath(filepath, '.')
                zipf.write(relative_path)
                
    print(f"Archive successfully created at {os.path.abspath(zip_name)}")

if __name__ == "__main__":
    create_delivery_zip()

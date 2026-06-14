import os
import zipfile

def zip_project():
    output_zip = r"./LocalFoodAI_lanfr144.zip"
    base_dir = r"."
    food_dir = os.path.join(base_dir, "Food")
    
    print(f"Creating ZIP archive at: {output_zip}")
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED, allowZip64=True ) as zipf:
        # 1. Zip parent folder planning documents
        parent_docs = [
            "todo.docx",
            "domainproject.pdf",
            "BTS-AI DOPRO Course Catalogue.pdf",
            "The_Scrum_Master_Training_Manual_A_Guide.pdf"
        ]
        
        print("Archiving parent planning and project documents...")
        for doc in parent_docs:
            doc_path = os.path.join(base_dir, doc)
            if os.path.exists(doc_path):
                # Write to root of the ZIP
                zipf.write(doc_path, arcname=doc)
                print(f"  Added: {doc}")
            else:
                print(f"  WARNING: {doc} not found, skipping.")
                
        # 2. Zip the entire Food directory recursively
        print("Archiving Food codebase (excluding .venv and caches)...")
        exclude_dirs = {".venv", "__pycache__", ".git"}
        
        for root, dirs, files in os.walk(food_dir):
            # Prune directories in-place to exclude .venv, .git, and __pycache__
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                # Do not zip the temporary scratch scripts or ZIP itself if created there
                file_path = os.path.join(root, file)
                # Compute relative path inside the zip file
                rel_path = os.path.relpath(file_path, base_dir)
                zipf.write(file_path, arcname=rel_path)
                
        print("ZIP archive successfully completed!")

if __name__ == "__main__":
    zip_project()

#!/usr/bin/env python3
#ident "@(#)$Format:LocalFoodAI:create_delivery_zip.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import zipfile
import pathspec

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gitignore_path = os.path.join(repo_root, ".gitignore")
    
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, f)
    else:
        spec = pathspec.PathSpec([])
        
    # Standard ignores
    spec.patterns.append(pathspec.patterns.GitWildMatchPattern('.git/'))
    spec.patterns.append(pathspec.patterns.GitWildMatchPattern('*.zip'))

    zip_path = os.path.join(repo_root, "delivery.zip")
    print(f"Building {zip_path}...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(repo_root):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_root)
                posix_path = rel_path.replace(os.sep, '/')
                
                # Check against .gitignore rules
                if not spec.match_file(posix_path):
                    zipf.write(full_path, rel_path)
                    
    print(f"Successfully created: delivery.zip")

if __name__ == "__main__":
    main()

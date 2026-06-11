#!/usr/bin/env python
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import shutil

def archive_scratch():
    # Define directories
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scratch_dir = os.path.join(base_dir, "scratch")
    user_profile = os.environ.get("USERPROFILE") or os.path.expanduser("~")
    keep_dir = os.path.join(user_profile, "keep")

    # Create destination folder if not exists
    if not os.path.exists(keep_dir):
        os.makedirs(keep_dir)
        print(f"Created archive directory: {keep_dir}")

    # Check scratch directory contents
    if not os.path.exists(scratch_dir):
        print(f"Scratch directory does not exist: {scratch_dir}")
        return

    # Move files
    files_moved = 0
    for filename in os.listdir(scratch_dir):
        src_path = os.path.join(scratch_dir, filename)
        
        # Skip directories if any
        if not os.path.isfile(src_path):
            continue

        # Find unique versioned filename
        version = 1
        while True:
            # First file is named test_filter.py;001, then test_filter.py;002...
            dest_filename = f"{filename};{version:03d}"
            dest_path = os.path.join(keep_dir, dest_filename)
            if not os.path.exists(dest_path):
                break
            version += 1

        shutil.move(src_path, dest_path)
        print(f"Moved: {filename} -> {dest_path}")
        files_moved += 1

    print(f"Scratch archiving completed. Total files archived: {files_moved}")

if __name__ == "__main__":
    archive_scratch()
#!/usr/bin/env python
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import sys
import os
import subprocess
import re
from datetime import datetime

# Force LF-only line endings on Windows for stdin and stdout to prevent automatic CRLF translation
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(newline='\n')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(newline='\n')

# Detect execution mode (clean or smudge) passed by Git
mode = sys.argv[1] if len(sys.argv) > 1 else "smudge"

def get_git_info(file_path):
    """Retrieves commit metadata for the specific file using git log, or falls back to system context."""
    try:
        # 1. Query git log for the last commit details of the specific file
        cmd = [
            "git", "log", "-1",
            "--date=format:%Y/%m/%d %H:%M:%S",
            "--format=%an|%ae|%ad|%cn|%ce|%cd|%H|%D|%N",
            "--", file_path
        ]
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip()
        if out:
            parts = out.split('|')
            if len(parts) == 9:
                return parts
    except Exception:
        pass
    
    # 2. Fallback: Query local Git configuration if file is not committed yet
    try:
        author_name = subprocess.check_output(["git", "config", "user.name"], stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip() or "system"
        author_email = subprocess.check_output(["git", "config", "user.email"], stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip() or "system@mail.com"
    except Exception:
        author_name = "system"
        author_email = "system@mail.com"
        
    now_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return [author_name, author_email, now_str, author_name, author_email, now_str, "Not Committed Yet", "local", "none"]

if mode == "clean":
    # CLEAN Mode: Replaces any smudged $Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$ tag back to the standard neutral git representation
    content = sys.stdin.read()
    # Non-greedy substitution to restore standard placeholder format for Git storage
    cleaned = re.sub(
        r'\$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$)?[^$]*?\$', 
        r'$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$', 
        content
    )
    sys.stdout.write(cleaned)

else:
    # SMUDGE Mode: Dynamically injects actual project, file path, and commit metadata into the file
    try:
        # Get absolute path of repository to find project directory name
        toplevel = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL).decode().strip()
        project_name = os.path.basename(toplevel)

        # Get the relative path of the file being smudged
        file_name = sys.argv[2] if len(sys.argv) > 2 else "unknown_file"

        # Read the file content sent by Git on stdin
        content = sys.stdin.read()

        # Query git log metadata or local fallbacks
        info = get_git_info(file_name)

        # Format replacement string using LocalFoodAI and app.py
        replacement = f"$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

        # Regex replacement targeting the dynamic format placeholders
        smudged = re.sub(
            r'\$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$', 
            replacement, 
            content
        )
        sys.stdout.write(smudged)

    except Exception:
        # Security fallback: If executed outside Git repo, write stream unchanged
        sys.stdout.write(sys.stdin.read())
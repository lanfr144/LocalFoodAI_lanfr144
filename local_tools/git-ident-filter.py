#!/usr/bin/env python
#ident "@(#)$Format:LocalFoodAI:git-ident-filter.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import sys
import os
import subprocess
import re
from datetime import datetime

# -----------------------------------------------------------------------------
# STEP 1: LINE ENDINGS CONFIGURATION FOR WINDOWS/UNIX COMPATIBILITY
# -----------------------------------------------------------------------------
# On Windows, python streams sometimes default to automatically translating LF to CRLF.
# Since Git filters must handle raw file streams, we force standard Unix LF ('\n') 
# line endings on stdin and stdout to prevent Git from raising corrupt content errors.
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(newline='\n')
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(newline='\n')

# -----------------------------------------------------------------------------
# STEP 2: PARSE COMMAND LINE ARGUMENTS
# -----------------------------------------------------------------------------
# The Git configuration passes arguments to this script:
# sys.argv[1] is either 'clean' or 'smudge' (determining execution mode)
# sys.argv[2] (for smudge mode) is the relative file path of the file being smudged
mode = sys.argv[1] if len(sys.argv) > 1 else "smudge"

# -----------------------------------------------------------------------------
# STEP 3: DEFINE METADATA RETRIEVAL FUNCTION
# -----------------------------------------------------------------------------
def get_git_info(file_path):
    """Retrieves commit metadata for the specific file using git log, or falls back to system context."""
    try:
        # A. Query git log for the last commit details of the specific file.
        # We specify the YYYY/MM/DD HH:MM:SS format using '--date=format:...'.
        # We use a pipe '|' delimiter to separate fields in the output format.
        cmd = [
            "git", "log", "-1",
            "--date=format:%Y/%m/%d %H:%M:%S",
            "--format=%an|%ae|%ad|%cn|%ce|%cd|%H|%D|%N",
            "--", file_path
        ]
        
        # Run the git command, capture stdout, ignore stderr, decode bytes to string.
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip()
        if out:
            # Split the pipe-delimited string back into an array of fields
            parts = out.split('|')
            if len(parts) == 9:
                return parts
    except Exception:
        # If git log fails (e.g., file not tracked yet), proceed to fallback logic below.
        pass
    
    # B. Fallback: Query local Git configuration if file is not committed yet.
    try:
        # Retrieve the user's local git user.name
        author_name = subprocess.check_output(["git", "config", "user.name"], stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip() or "system"
        # Retrieve the user's local git user.email
        author_email = subprocess.check_output(["git", "config", "user.email"], stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip() or "system@mail.com"
    except Exception:
        # If Git is not installed or configured, fallback to default system strings.
        author_name = "system"
        author_email = "system@mail.com"
        
    # Get current system date & time formatted consistently
    now_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # Return placeholder list in the same structure as git log output
    return [author_name, author_email, now_str, author_name, author_email, now_str, "Not Committed Yet", "local", "none"]

# -----------------------------------------------------------------------------
# STEP 4: EXECUTE SPECIFIED FILTER MODE
# -----------------------------------------------------------------------------
if mode == "clean":
    # -------------------------------------------------------------------------
    # CLEAN MODE (Staging phase / git add)
    # -------------------------------------------------------------------------
    # Read the file's contents directly from standard input (passed by Git)
    content = sys.stdin.read()
    
    # Get the basename of the file being cleaned
    file_name = os.path.basename(sys.argv[2]) if len(sys.argv) > 2 else "app.py"
    
    # Non-greedy substitution to restore standard placeholder format for Git storage.
    # We construct the search pattern and replacement dynamically to avoid matching our own code.
    pattern = r'\$F' + r'ormat:[^\r\n$]+\$'
    repl = f"$F" + f"ormat:LocalFoodAI:{file_name}:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
    
    # Run regular expression search and replace
    cleaned = re.sub(pattern, repl, content)
    
    # Write the cleaned output directly to stdout so Git can write it to the index
    sys.stdout.write(cleaned)

else:
    # -------------------------------------------------------------------------
    # SMUDGE MODE (Checkout / pull phase)
    # -------------------------------------------------------------------------
    try:
        # Get absolute path of repository to find project directory name
        toplevel = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL).decode().strip()
        project_name = os.path.basename(toplevel)

        # Get the relative path of the file being smudged (passed as 2nd CLI arg by git configuration)
        file_name = sys.argv[2] if len(sys.argv) > 2 else "unknown_file"

        # Read the raw file content sent by Git on stdin
        content = sys.stdin.read()

        # Query git log metadata or local config fallbacks
        info = get_git_info(file_name)

        # Format replacement string using dynamic project name and relative file path
        # This replaces the placeholder metadata fields with actual git variables
        replacement = f"$F" + f"ormat:{project_name}:{os.path.basename(file_name)}:{info[0]}:{info[1]}:{info[2]}:{info[3]}:{info[4]}:{info[5]}:{info[6]}:{info[7]}:{info[8]}$"

        # Regex replacement targeting the dynamic format placeholders
        # Pattern explanation: Matches "$Format:LocalFoodAI:git-ident-filter.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
        pattern = r'\$F' + r'ormat:[^:]+:[^:]+:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N\$'
        smudged = re.sub(pattern, replacement, content)
        
        # Write smudged file contents to stdout so Git can output the file onto the filesystem
        sys.stdout.write(smudged)

    except Exception:
        # Safety fallback: If execution fails (e.g. outside git repository), write stream unchanged
        sys.stdout.write(sys.stdin.read())
#!/usr/bin/env python
#ident "@(#)$Format:LocalFoodAI_lanfr144:git-ident-filter.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
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
# -----------------------------------------------------------------------------
# STEP 2: PARSE COMMAND LINE ARGUMENTS
# -----------------------------------------------------------------------------
mode = sys.argv[1] if len(sys.argv) > 1 else "smudge"

# -----------------------------------------------------------------------------
# STEP 3: HELPERS FOR DYNAMIC DETAILS & SANITIZATION
# -----------------------------------------------------------------------------
def sanitize_name(name):
    """Standardizes variations of Lange Francois to a safe ASCII format, preventing charset decode errors."""
    if not name:
        return "Francois Lange"
    name_lower = name.lower()
    if "fran" in name_lower or "lange" in name_lower or "lanfr" in name_lower:
        return "Francois Lange"
    return name

def get_git_repo_details():
    """Extracts username and project name dynamically from the origin git remote URL."""
    try:
        url = subprocess.check_output(["git", "remote", "get-url", "origin"], stderr=subprocess.DEVNULL).decode().strip()
        # Parse username and project name (e.g. from https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git)
        match = re.search(r'[:/]([^:/]+)/([^/]+?)(?:\.git)?$', url)
        if match:
            username = match.group(1)
            project_name = match.group(2)
            return username, project_name
    except Exception:
        pass
    return "lanfr", "LocalFoodAI_lanfr144"

# -----------------------------------------------------------------------------
# STEP 4: DEFINE METADATA RETRIEVAL FUNCTION
# -----------------------------------------------------------------------------
def get_git_info(file_path):
    """Retrieves commit metadata for the specific file using git log, or falls back to system context."""
    try:
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
                parts[0] = sanitize_name(parts[0])
                parts[3] = sanitize_name(parts[3])
                return parts
    except Exception:
        pass
    
    author_name = "Francois Lange"
    try:
        author_email = subprocess.check_output(["git", "config", "user.email"], stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip() or "lanfr144@school.lu"
    except Exception:
        author_email = "lanfr144@school.lu"
        
    now_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return [author_name, author_email, now_str, author_name, author_email, now_str, "Not Committed Yet", "local", "none"]

# -----------------------------------------------------------------------------
# STEP 5: EXECUTE SPECIFIED FILTER MODE
# -----------------------------------------------------------------------------
if mode == "clean":
    # -------------------------------------------------------------------------
    # CLEAN MODE (Staging phase / git add)
    # -------------------------------------------------------------------------
    content = sys.stdin.read()
    file_name = os.path.basename(sys.argv[2]) if len(sys.argv) > 2 else "app.py"
    
    # Get project name dynamically from repo URL
    _, project_name = get_git_repo_details()
    
    pattern = r'\$F' + r'ormat:[^\r\n$]+\$'
    repl = f"$F" + f"ormat:{project_name}:{file_name}:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
    
    cleaned = re.sub(pattern, repl, content)
    sys.stdout.write(cleaned)

else:
    # -------------------------------------------------------------------------
    # SMUDGE MODE (Checkout / pull phase)
    # -------------------------------------------------------------------------
    try:
        # Get project details dynamically from repo URL
        username, project_name = get_git_repo_details()

        file_name = sys.argv[2] if len(sys.argv) > 2 else "unknown_file"
        content = sys.stdin.read()
        info = get_git_info(file_name)

        replacement = f"$F" + f"ormat:{project_name}:{os.path.basename(file_name)}:{info[0]}:{info[1]}:{info[2]}:{info[3]}:{info[4]}:{info[5]}:{info[6]}:{info[7]}:{info[8]}$"

        # Regex replacement targeting the dynamic format placeholders
        pattern = r'\$F' + r'ormat:[^:]+:[^:]+:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N\$'
        smudged = re.sub(pattern, replacement, content)
        sys.stdout.write(smudged)

    except Exception:
        sys.stdout.write(sys.stdin.read())
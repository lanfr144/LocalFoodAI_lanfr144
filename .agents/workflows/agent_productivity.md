---
description: AI Agent environment productivity, paths, and git rules
---

# Agent Workflow: Productivity & Safety Guidelines

This workflow provides critical instructions for autonomous agents when running commands, configuring paths, and managing Git operations in this repository.

## Rule 1: Execute Non-Interactive Commands
* **Context:** Agents running terminal commands do not have interactive input access to pipe standard input prompts (like `sudo` password requests).
* **Action:**
  1. **Strictly avoid** running interactive commands.
  2. Always use non-interactive flags (e.g., `docker exec -d`, `npm install -y`, `apt-get install -y`).
  3. Sourcing credentials must be done via reading the `.env` file instead of prompting.

## Rule 2: Git Mirror Privacy Check
* **Context:** Command-line pushes to GitHub mirror repositories will fail with error `GH007` if the user's local git commits expose a private/protected email address.
* **Action:**
  1. Before executing `git push` to a GitHub mirror, check if the developer's git configuration matches their GitHub account's public email settings.
  2. If a mirror push fails with `GH007`, instruct the user to temporarily disable **"Block command line pushes that expose my email"** under their GitHub profile settings page: `https://github.com/settings/emails`.

## Rule 3: Use Absolute Paths with Forward Slashes
* **Context:** Windows and WSL handle paths differently (e.g. `C:\...` vs `/mnt/c/...`). Rendering and layout engines (like MuPDF/PyMuPDF or Docker mounts) fail when using backslashes (`\`) or relative paths.
* **Action:**
  1. Always resolve paths dynamically using Python's `os.path.abspath()`.
  2. Normalize all path strings by replacing backslashes with forward slashes: `.replace('\\', '/')`.
  3. Write absolute forward-slash paths inside configurations (like `@font-face` styles or Docker compose scripts) to guarantee compatibility across Windows, WSL, and Linux containers.

## Rule 4: Safely Recover from Git Filter Loops
* **Context:** Clean/smudge attributes filters can trigger checkout loops if the filter script (`local_tools/git-ident-filter.py`) is missing from the working directory during checkout.
* **Action:**
  1. If `git checkout` fails with filter errors, restore the filter script first from the HEAD commit:
     ```bash
     git checkout HEAD -- local_tools/git-ident-filter.py
     ```
  2. Once the script is restored, re-run the clean checkout:
     ```bash
     git checkout -f
     ```

## Rule 5: Keep Credentials Ignored
* **Context:** Temporary scripts containing tokens (such as `add_mirror_repos.bat` with a `GITHUB_TOKEN`) must never be committed.
* **Action:**
  1. Always save temporary scripts containing credentials in the `scratch/` directory.
  2. The `scratch/*` rule inside `.gitignore` will automatically prevent these scripts from being tracked or pushed.

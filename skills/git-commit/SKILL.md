The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:SKILL.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

---
name: git-commit
description: Enforces strict Git governance, Taiga tracking, branching strategies, and file metadata standards.
---

# Git Commit Governance Skill

When analyzing git commits, pull requests, or branch merges, you must strictly enforce the following rules:

## 1. Commit Messages & Tracking
- **Taiga Integration:** Every commit message MUST start with the specific Taiga task/story tag (e.g., `TG-123`, `US#123`, or `[#123]`) to update the task status. You must ensure a Git hook is actively verifying this format and rejecting non-compliant commits.

## 2. Branching Strategy & Segregation of Duties
- **Pipeline Flow:** Verify the code progresses strictly through three branches: `development` -> `test` (or `integration`) -> `production`.
- **WARNING - Segregation of Duties:** Since the current team size is small, DO NOT block the merge. Instead, **provide a warning** if the user attempting to promote/merge the code is the same user who originally authored the code, or if they are bypassing a branch.
- **WARNING - Cross-Branch Promotion:** You must issue a warning if the same user is attempting to promote files from one branch directly to another without proper review gates.

## 3. File Metadata & Formatting
* **Header Tag Requirement:** Every source code, scripting, config, or text file (including ignored scratch files) must include the exact identity format at the top of the file:
```text
i d e n t   " @ ( # ) $ F o r m a t : { p r o j e c t _ n a m e } : { f i l e _ n a m e } : % a n : % a e : % a d : % c n : % c e : % c d : % H : % D : % N $ "
```
*Note: In the template above, the character sequence has been intentionally formatted with spaces between each character (representing the `sed` transformation `s/./& /g`). This prevents Git's clean/smudge filters from matching, interpreting, and modifying this rule documentation file itself.*
  For tracked files, the Git smudge filter (`ident-dynamic`) will automatically expand the placeholder variables with real Git commit and author/committer data during checkouts. Untracked or ignored scratch files must still physically carry this header comment as a repository consistency requirement.
  The comment syntax must match the file's language (e.g., `#` for Python/Shell/YAML/Markdown/Dockerfiles, `--` for SQL, `::` for Batch). For tracked files, the git smudge filter expands this dynamically. Ignore-listed/scratch files must carry the comment statically for structure.
  Adapt the comment syntax (e.g., "//", "#", "--", "`", "!", "REM", "/*  */") to the specific language. Exception: For executable scripts requiring a shebang (e.g., #!/bin/bashor#!/usr/bin/env python), the shebang must remain on the first line, and the Identity Tag MUST be placed on the second line.

  To initialize a new file, place the clean version at the top of your file (legible examples are listed below in spaced-out format to prevent active smudge filter matching):
- For Python/Shell files:
  `# i d e n t   " @ ( # ) $ F o r m a t : G i t  p r o j e c t   n a m e : f i l e n a m e : % a n : % a e : % a d : % c n : % c e : % c d : % H : % D : % N $ "`
- For SQL files:
  `- - i d e n t   " @ ( # ) $ F o r m a t : G i t  p r o j e c t   n a m e : f i l e n a m e : % a n : % a e : % a d : % c n : % c e : % c d : % H : % D : % N $ "`
- For Batch files:
  `: : i d e n t   " @ ( # ) $ F o r m a t : G i t  p r o j e c t   n a m e : f i l e n a m e : % a n : % a e : % a d : % c n : % c e : % c d : % H : % D : % N $ "`
- For Markdown/YAML/Dockerfiles/XML:
  `# i d e n t   " @ ( # ) $ F o r m a t : G i t  p r o j e c t   n a m e : f i l e n a m e : % a n : % a e : % a d : % c n : % c e : % c d : % H : % D : % N $ "`
- **Line Endings:** Only Line Feed (LF) is allowed (Carriage Return Line Feed (CRLF) is strictly forbidden), with the exception of Windows batch files (`*.bat`), which must use CRLF. Exception: For executable scripts requiring a shebang (e.g., #!/bin/bash or #!/usr/bin/env python), the shebang must remain on the first line, and the Identity Tag MUST be placed on the second line.

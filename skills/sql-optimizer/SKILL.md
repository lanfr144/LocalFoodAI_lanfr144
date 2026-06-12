The current version is #ident "@(#)$Format:DEVOP1:skills/sql-optimizer/SKILL.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

---
name: sql-optimizer
description: Optimizes and secures SQL for MySQL, Oracle, and PostgreSQL, enforcing strict DBA standards.
---

# SQL Optimizer & DBA Skill

When reviewing, optimizing, or generating SQL code (MySQL, Oracle, PostgreSQL), enforce these strict database guidelines:

## 1. Performance & Concurrency
- **Locking:** Avoid row locking issues and design queries to prevent deadlocks.
- **Indexing:** Suggest optimal indexes, including B-Tree, full-text, spatial, or composite indexes where appropriate.
- **Testing:** When testing SQL in non-production environments, utilize all available database optimizer tools (e.g., `EXPLAIN PLAN`, `tkprof`).

## 2. Security & Access Control
- **No Hardcoded Users:** NEVER hardcode usernames in scripts.
- **Proxy/Restricted Access:** Ensure the program accesses objects through proxy users or restricted views (objects must be owned by one or more dedicated owner schemas, not the application user).
- **Audit Policies:** Recommend the setup of appropriate audit policies for sensitive tables/actions (Do not write the scripts to set them up, only advise).
- **Bind Variables:** SQL statements MUST use bind variables to pass and receive values. No dynamic concatenation of user inputs.
- **Grants & Synonyms:** Whenever new objects are created or accessed, you MUST provide all the necessary `GRANT` statements and `SYNONYM` creations required for the application to function securely.
## 3. Transaction Management
- **No Auto-Commit:** Disable auto-commit. Explicitly manage transactions with `COMMIT` and `ROLLBACK` blocks.

## 4. Syntax & DDL Standards
- **Quoted Identifiers:** All object and column names must be double-quoted (`"`) or back-quoted (`` ` ``) to avoid collisions with reserved words. Warn if a name matches a `V$RESERVED_WORDS` in Oracle.
- **Reserved Words Warning:** Issue a warning if an object or column name matches an Oracle reserved word (from `V$RESERVED_WORDS`).
- **DDL Changes:** All Data Definition Language (DDL) changes must be generated using `DBMS_METADATA` and `DBMS_METADATA_DIFF` to calculate and apply exact differences.
- **Exception Management:** Always implement robust exception handling (e.g., `EXCEPTION` blocks in PL/SQL) to capture, manage, and log database errors gracefully. Do not allow silent failures.

## 5. Mandatory File Header
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


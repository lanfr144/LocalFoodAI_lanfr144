import os

skills_dir = "skills"
for root, dirs, files in os.walk(skills_dir):
    for f in files:
        if f.endswith(".md"):
            path = os.path.join(root, f)
            with open(path, "rb") as file_handle:
                content = file_handle.read()
                has_crlf = b"\r\n" in content
                has_lf = b"\n" in content and not has_crlf
                print(f"{path}: CRLF={has_crlf}, LF={has_lf}, length={len(content)}")

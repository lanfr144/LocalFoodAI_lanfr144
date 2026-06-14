with open("app.py", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if "ACTIVE_MODEL" in line:
            print(f"Line {i}: {line.strip()}")

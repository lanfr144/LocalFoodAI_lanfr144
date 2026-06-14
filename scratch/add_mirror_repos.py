import os

# 1. Update INSTALL_WSL.md
file1 = "INSTALL_WSL.md"
if os.path.exists(file1):
    with open(file1, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    
    old_clone_block = """### Step 2: Clone the Git Repository
Run the following commands inside your WSL Ubuntu home directory to clone the project:
```bash
git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git
cd LocalFoodAI_lanfr144
```"""

    new_clone_block = """### Step 2: Clone the Git Repository
Run the following commands inside your WSL Ubuntu home directory to clone the project:

**Primary Repository (Internal Network)**:
```bash
git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git
cd LocalFoodAI_lanfr144
```

**Alternative Repository (Worldwide Access - Clone of the Primary)**:
```bash
git clone https://github.com/lanfr144/LocalFoodAI_lanfr144.git
cd LocalFoodAI_lanfr144
```"""

    content = content.replace(old_clone_block, new_clone_block)
    with open(file1, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated INSTALL_WSL.md with mirror repositories.")

# 2. Update generate_docs.py
file2 = "generate_docs.py"
if os.path.exists(file2):
    with open(file2, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Update Installation_Guide.md section in generate_docs.py
    old_install_repos = """There are two repositories configured for this project:
- Production Repository: `https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git`
- GitHub Mirror (Clone): `https://github.com/lanfr144/LocalFoodAI_lanfr144`"""

    new_install_repos = """There are two repositories configured for this project:
- Primary Git Repository: `https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git`
- Alternative Git Repository (Worldwide Access - Clone): `https://github.com/lanfr144/LocalFoodAI_lanfr144.git`"""

    content = content.replace(old_install_repos, new_install_repos)

    # Update Technical_Document.md section in generate_docs.py
    old_tech_repos = """- *Online Mode*: `git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git`"""
    new_tech_repos = """- *Online Mode (Primary)*: `git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git`
   - *Online Mode (Alternative/Worldwide)*: `git clone https://github.com/lanfr144/LocalFoodAI_lanfr144.git`"""

    content = content.replace(old_tech_repos, new_tech_repos)

    with open(file2, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated generate_docs.py with mirror repositories.")

# 3. Update README.md
file3 = "README.md"
if os.path.exists(file3):
    with open(file3, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    old_readme_repos = """2. **Branch Checkout & App Setup (WSL Environment)**:
   Navigate to the repository home directory inside WSL:
   ```bash
   cd ~
   git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git
   cd LocalFoodAI_lanfr144"""

    new_readme_repos = """2. **Branch Checkout & App Setup (WSL Environment)**:
   Navigate to the repository home directory inside WSL:
   ```bash
   cd ~
   # Option A: Clone from the Primary Repository (Internal Network)
   git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git
   
   # Option B: Clone from the Alternative Repository (Worldwide Access - Clone)
   # git clone https://github.com/lanfr144/LocalFoodAI_lanfr144.git
   
   cd LocalFoodAI_lanfr144"""

    content = content.replace(old_readme_repos, new_readme_repos)
    with open(file3, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated README.md with mirror repositories.")

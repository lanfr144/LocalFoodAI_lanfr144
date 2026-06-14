import os

file_path = "README.md"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
    
    # Clean encoding issue
    content = content.replace("Lange FranA ois", "Francois Lange")
    content = content.replace("Lange FranAois", "Francois Lange")
    content = content.replace("Lange François", "Francois Lange")
    
    old_doc_part = """## Documentation (Capstone Deliverables)
Please refer to the `docs/` folder for detailed guides:
- [Architecture Map](docs/architecture.md)"""

    new_doc_part = """## Documentation (Capstone Deliverables)
Please refer to the `docs/` folder for detailed guides:
- [Detailed WSL Installation Guide (PDF)](docs/Installation_Guide.pdf) | [Markdown Version](docs/Installation_Guide.md)
- [Architecture Map](docs/architecture.md)"""

    content = content.replace(old_doc_part, new_doc_part)

    quick_start = """
## Quick Start & WSL Installation

This project is fully optimized to run on Windows Subsystem for Linux (WSL2) with Ubuntu 22.04 LTS.

1. **WSL Setup (Windows Host)**:
   Open an Administrator PowerShell window at the root of the repository and run:
   ```powershell
   powershell.exe -ExecutionPolicy Bypass -File setup_wsl.ps1
   ```
   *This enables WSL2 features and spins up a dedicated Ubuntu 22.04 LTS instance named `Dopro1` with user `lanfr144`.*

2. **Branch Checkout & App Setup (WSL Environment)**:
   Navigate to the repository home directory inside WSL:
   ```bash
   cd ~
   git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git
   cd LocalFoodAI_lanfr144
   
   # Always ensure you are on the primary main branch:
   git checkout main
   
   # Launch the installation script to set up Docker, configurations, and permissions:
   ./setup_app.sh
   ```
   
3. **Run services**:
   Configure database and app variables in a `.env` file at the root directory, then run:
   ```bash
   ./manage_services.sh start
   ```

For detailed step-by-step instructions, please consult the [Installation Guide PDF](docs/Installation_Guide.pdf).
"""

    # Add quick start before Tech Stack
    content = content.replace("## Tech Stack", quick_start + "\n## Tech Stack")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("README.md successfully updated.")

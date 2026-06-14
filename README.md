The current version is #ident "@(#)$Format:LocalFoodAI:README.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

# Local Food AI 🍔

A strictly local, privacy-first AI Medical Dietitian and Food Explorer. This project leverages the OpenFoodFacts dataset and local LLMs (Ollama) to provide medically sound dietary advice, recipe parsing, and menu planning without sending any user data to the cloud.

## Features
- **Dynamic Medical Profiling**: Configure your health profile (e.g., Kidney issues, pregnancy, vegan). The AI dynamically adjusts all responses, recommendations, and warnings based on these exact medical needs.
- **RAG Architecture**: The AI is connected to a massively partitioned local MySQL database. When you ask a question or request a meal plan, the AI executes SQL queries autonomously to fetch precise nutritional data.
- **SearXNG Web Integration**: When the local Database lacks culinary heuristics, the AI securely queries a local, private instance of SearXNG to answer questions without compromising patient privacy.
- **Plate Builder & Unit Conversion**: Input culinary recipes (e.g., "1.5 cups of flour") and the system converts them to metric standard weights based on the product's density.
- **Distributed Microservice Topology**: Supports decoupling across VirtualBox, Hyper-V, and WSL2 using Bridged Networking and SNMP container telemetry for Zabbix.

## Documentation (Capstone Deliverables)
Please refer to the `docs/` folder for detailed guides:
- [Detailed WSL Installation Guide (PDF)](docs/Installation_Guide.pdf) | [Markdown Version](docs/Installation_Guide.md)
- [Architecture Map](docs/architecture.md)
- [Distributed Deployment Procedure (PoC)](docs/distributed_deployment.md)
- [Disaster Recovery & Backup Plan](docs/disaster_recovery_plan.md)
- [Zabbix Telemetry Guide](docs/zabbix_monitoring.md)
- [Agile Retro Planning](docs/retro_planning.md)
- [Taiga Final Audit Report](docs/taiga_audit_report.md)
- [Historical Taiga Agile Export](taiga/local-food-ai-1-5947063a-612b-454f-b3f1-6b5858445510.json) (included strictly for documentation and project history purposes)


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

## Tech Stack
- **Frontend**: Streamlit
- **Database**: MySQL 8.0
- **AI Engine**: Ollama (Llama 3.2:3B)
- **Web Search**: SearXNG
- **Monitoring**: Zabbix (SNMPv2c)
- **Deployment**: Native Ubuntu, Docker Compose, Hyper-V / VirtualBox
- **Project Management**: Taiga (Synced dynamically via Python)

## AI Skills & Governance
This project leverages specialized AI skills to maintain code quality, documentation, and strict governance:
- **Code Review**: Automatically reviews code changes for correctness, edge cases, style, and performance.
- **Doc Writer**: Ensures all documentation and inline comments stay perfectly synchronized with source code changes.
- **Expert Coach**: Acts as a principal engineer, enforcing optimal code, modularity, and a mandatory Identity Tag in file headers.
- **Git Commit**: Enforces strict Git governance, Taiga tracking (`TG-123`), and a single `main` branch workflow. For every commit, a task in Taiga must be associated. If the task does not exist, it must be created and added to a user story and a sprint.
- **Refactor Coach**: Refactors code to improve readability, performance, and modularity without changing external behavior.
- **SQL Optimizer**: Enforces DBA standards for MySQL, Oracle, and PostgreSQL, ensuring proper indexing, transaction management, and secure access.
- **Test Generator**: Generates comprehensive unit and integration tests focusing on boundary conditions and logical coverage.

## Grading

There will be 6 grades in total: 3 for Project Management 1 (PM1) and 3 for Domain-specific Project 1 (DSP1).

### PM1:
* Requirements analysis and assessment.
* Overall project planning and execution.
* Project presentation.

### DSP1:
* The final product shipped to the customer.
* The product documentation:
  * **Technical document**, explaining how to install and configure the final product as well as the technologies used (LLM, DB, etc.) for an IT audience. Explain which Antigravity models you used for which tasks as well as how and why you configured agent permissions. Also reflect on what Antigravity struggled with and you handled this. Explain which local LLM the app uses and why. Explain the app infrastructure via a diagram showing how the app components communicate locally. Explain how you've verified that no user data leaves the server.
  * **User manual**, explaining how to use the final product from an end user (non developer) perspective.
* The presentation to the customer.

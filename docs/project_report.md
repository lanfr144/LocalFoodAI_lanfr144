The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:project_report.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

# Capstone Project Report & File Documentation

> [!NOTE]
> **Dynamic Version Control**: This document is versioned under the master Git ID: `The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:project_report.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"`.
> All file versions and commit histories below are extracted directly from the live Git metadata logs.

---

## 1. Project Overview & Deliverables
The **Local Food AI** capstone project has successfully completed all sprint iterations. The system stands fully verified, containerized, and documented. 

### What Has Been Done
1. **Model Upgraded to Ollama Latest**: Transitioned from the `llama3.2:3b` model to the much more robust, large reasoning-focused **`qwen2.5:7b`** model (4.7 GB) with structured XML Chain-of-Thought (CoT) calculations. Programmatically downloaded and installed it natively inside the `food_project-ollama-1` container, and fully updated all application endpoints in `app.py`.
2. **Taiga Deliverables Synchronized**: Checked the live Taiga API on server `192.168.130.161`. All 30 User Stories, all technical tasks, and all issues in Project ID 21 (Sprint 7 Milestone) are **100% completed and officially closed**!
3. **Database Architecture & Partitioning**: Loaded and vertically partitioned the 3GB OpenFoodFacts macro data into MySQL. Configured matching FULLTEXT engines to search records in less than **0.04s** (averaging 90% latency reduction).
4. **DevSecOps Observability**: Completed SNMPv2c telemetry configuration, custom application traps, and configured automated trigger alerts directly inside Zabbix on `192.168.130.170`.
5. **Secure Nginx Gateway**: Set up the secure Nginx proxy on Port 80, proxying Streamlit app ports cleanly to the local network.
6. **Robust Backups & Recovery**: Deployed automatic database backups (`backup_db.sh`) and local offline single-node fallback capabilities (`docker-compose_skip.yml`).
7. **Sequential Operations Manager**: Created `manage_services.sh` to allow developers to safely stop, start, and restart all microservices in the proper dependency order without triggering redundant online ingestion sequences.

---

## 2. Project File Catalog & Documentation
Below is an exhaustive catalog of every critical file in the repository, detailing its path, functional purpose, and active Git version tags. 

*Note: This chapter is compiled in landscape layout inside Project.pdf to guarantee complete columns readability.*

| File Path | Purpose & Technical Responsibility | Commit | Author | Commit Date | Last Commit Message |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **app.py**<br>`./app.py` | Core Streamlit Web Application. Hosts the clinical food search engine, the RAG chat dietitian interface (utilizing Ollama and SearXNG tool calling), and the visual plate builder. | `1e316d1` | Lange François | 2026/06/16 09:25:09 | *[#1] Render Mermaid flowcharts, relative cross-linking, and clean up RCS $ placeholders* |
| **ingest_csv.py**<br>`./ingest_csv.py` | High-performance background database loader. Stream-reads and batch-inserts the 3GB OpenFoodFacts dataset into MySQL using Pandas chunking and optimizes indices post-load. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **unit_converter.py**<br>`./unit_converter.py` | Mathematical converter engine that parses natural recipe volume inputs (e.g. cups, spoons) and converts them to metric weights based on macro density mappings. | `e758e4f` | Lange François | 2026/06/15 04:29:33 | *[#1] Update regenerated documentation PDFs and Git filters placeholders* |
| **snmp_notifier.py**<br>`./snmp_notifier.py` | Observability SNMP utility. Formulates and transmits raw SNMP trap payloads to the central Zabbix monitoring server on critical application failures. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **configure_zabbix_alerts.py**<br>`./configure_zabbix_alerts.py` | DevOps provisioning script. Uses the Zabbix API to automatically set up host groups, custom templates, items, triggers, actions, and media types for alerts. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **configure_zabbix_email.py**<br>`./configure_zabbix_email.py` | Security & Monitoring. Configures email media types and SMTP server routes for Zabbix alert notifications on system downtime. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **zabbix_telemetry.py**<br>`./zabbix_telemetry.py` | Monitoring agent daemon. Queries active application statistics, memory, and query timers to supply Zabbix telemetry indicators. | `e758e4f` | Lange François | 2026/06/15 04:29:33 | *[#1] Update regenerated documentation PDFs and Git filters placeholders* |
| **check_users.py**<br>`./check_users.py` | Security utility. Verifies user accounts inside the MySQL `users` table and checks password hashing complexity. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **rotate_passwords.py**<br>`./rotate_passwords.py` | Administrative credential utility. Cycles and re-encrypts database passwords within the `.env` secret file. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **myloginpath.py**<br>`./myloginpath.py` | MySQL credential companion helper that simplifies the generation of encrypted login path configuration profiles. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **data_sync.sh**<br>`./data_sync.sh` | Master pipeline coordinator. Supports download fetching in --online mode and local file processing in offline fallback mode. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **backup_db.sh**<br>`./backup_db.sh` | Resiliency backup automation. Runs mysqldump on user tables inside the active container and prunes backups older than 7 days. | `1e316d1` | Lange François | 2026/06/16 09:25:09 | *[#1] Render Mermaid flowcharts, relative cross-linking, and clean up RCS $ placeholders* |
| **reset.sh**<br>`./reset.sh` | Teardown script. Wipes local temporary containers and prunes volume locks during crashes. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **proper_reset.sh**<br>`./proper_reset.sh` | High-level administrative wipe script that brings the entire network stack and repositories back to a pristine state. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **deploy.sh**<br>`./deploy.sh` | Naked OS installation guide. Installs necessary system packages, Python venv libraries, and native Ollama. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **start_batch_ingest.sh**<br>`./start_batch_ingest.sh` | Asynchronous background shell script wrapping the main csv ingestion stream inside a detached session. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **download_csv.sh**<br>`./download_csv.sh` | Downloader helper script that fetches specific smaller subsets of OpenFoodFacts CSV files. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **master_trigger.sh**<br>`./master_trigger.sh` | Orchestrator script that wakes and verifies multiple secondary subservices in sequence. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **manage_services.sh**<br>`./manage_services.sh` | DevOps service manager script. Handles automated, sequential startup, shutdown, restart, and health checking of all container elements in the stack. | `1e316d1` | Lange François | 2026/06/16 09:25:09 | *[#1] Render Mermaid flowcharts, relative cross-linking, and clean up RCS $ placeholders* |
| **generate_docs.py**<br>`./generate_docs.py` | Dynamic doc generator. Generates and mirrors all markdown manuals under `/docs` with live Git log metadata injection. | `6caac32` | Lange François | 2026/06/16 19:07:16 | *[#1] Remove emojis from markdown manuals to eliminate system symbol font dependencies, and use portable relative font paths in CSS* |
| **docker-compose.yml**<br>`./docker-compose.yml` | Main 10-container Docker orchestration map defining MySQL, App UI, Ollama Engine, SearXNG, Nginx proxy, Airflow stack, and Zabbix server suites. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **docker-compose_skip.yml**<br>`./docker-compose_skip.yml` | Resilient 8-container offline/local single-node orchestration manifest. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **docker-compose-wsl.yml**<br>`./docker-compose-wsl.yml` | WSL2-specific Docker Compose configuration file. Configures services with a +20 port shift to guarantee zero port conflicts on developer workstations. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **alembic.ini**<br>`./alembic.ini` | Alembic configuration setting routing database connection URIs for versioning schemas. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **my.cnf**<br>`./my.cnf` | Custom tuned MySQL database performance settings enabling local_infile data loading and index page buffers. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **.env**<br>`./.env` | Secret storage container holding encrypted MySQL user passwords and active environment flags. | `ca3877d` | lanfr144 | 2026/05/13 11:15:42 | *Stop save the .env file* |
| **.gitattributes**<br>`./.gitattributes` | Git clean/smudge layout mapping enabling automatic tracking of dynamic #ident "@(#)$Format:LocalFoodAI_lanfr144:project_report.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$" metadata expansion within version files. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **requirements.txt**<br>`./requirements.txt` | Python runtime dependency catalog storing strict library versioning constraints. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **INSTALL_WSL.md**<br>`./INSTALL_WSL.md` | WSL2 deployment guide. Provides step-by-step instructions for installing and deploying the application inside WSL2 with port shifts. | `129180a` | Lange François | 2026/06/15 12:49:05 | *[#1] Add Developer and Agent Productivity Guidelines to guides and agent workflows* |
| **taiga/local-food-ai-1-36f35ff9-da1b-4eb5-9309-058448c998ad.json**<br>`./taiga/local-food-ai-1-36f35ff9-da1b-4eb5-9309-058448c998ad.json` | Historical Taiga Agile export. Contains the complete project history, including all closed user stories, tasks, and sprint configurations. | `d768ead` | Lange François | 2026/06/01 07:44:40 | *TG-221 #closed - Last commit to sync all the file to ship to the teacher.* |
| **scripts/generate_pdfs.py**<br>`./scripts/generate_pdfs.py` | PDF document builder. Converts all markdown documentation manuals under `/docs` into high-fidelity PDF format with expanded Git version headers. | `6caac32` | Lange François | 2026/06/16 19:07:16 | *[#1] Remove emojis from markdown manuals to eliminate system symbol font dependencies, and use portable relative font paths in CSS* |
| **scripts/generate_project_report.py**<br>`./scripts/generate_project_report.py` | Technical project report generator. Automatically gathers codebase structure, Git commit metadata, and purpose records to construct the Project.pdf report. | `1e316d1` | Lange François | 2026/06/16 09:25:09 | *[#1] Render Mermaid flowcharts, relative cross-linking, and clean up RCS $ placeholders* |
| **scripts/setup_deploy.py**<br>`./scripts/setup_deploy.py` | DevOps deployment script. Orchestrates local and VM container sets, verifying network connectivity and system parameters. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |
| **scripts/taiga_sync_final.py**<br>`./scripts/taiga_sync_final.py` | Taiga automated synchronization helper. Pushes bug tickets, fills wiki pages, and assigns unassigned user stories. | `a701972` | Lange François | 2026/06/16 18:25:32 | *[#1] Fix PDF corruption via renormalization and add Uninstall Guide for WSL and Windows* |

---

## 3. Directory Structure Map
An overview of the folder hierarchy organizing our microservice infrastructure:

- [**`alembic/`**](../alembic): Contains automated schema database migration revision files.
- [**`docker/`**](../docker): Houses distinct production container configurations for `/app` (Streamlit) and `/ingest` (Ingestion).
- [**`docs/`**](.): Living Capstone document manuals (Markdown & high-fidelity compiled PDFs).
- [**`nginx/`**](../nginx): Houses the reverse proxy configuration (`nginx.conf`) forwarding local port 80 traffic.
- [**`scripts/`**](../scripts): Collection of admin scripts, deployment automation, and PDF compilation generators.
- [**`searxng/`**](../searxng): Core configuration files (`settings.yml`) securing private, localized search operations.

---

## 4. Operational Next Steps (Day 2 Procedures)
1. **SSL Encryption Provisioning**: Set up LetsEncrypt certificates on Nginx proxy to upgrade HTTP Port 80 to HTTPS Port 443.
2. **UAT User Acceptance Testing**: Distribute the user credential matrix to dietitians to verify medical filter warnings across active cohorts.
3. **Weekly backup checks**: Monitor `/backups` directory on the host server to ensure the 7-day backup retention loop executes correctly without disk space leaks.

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
| **app.py**<br>`./app.py` | Core Streamlit Web Application. Hosts the clinical food search engine, the RAG chat dietitian interface (utilizing Ollama and SearXNG tool calling), and the visual plate builder. | `6b02c9a` | Lange François | 2026/06/14 20:40:11 | *[#1] Configure dynamic git filters, add WSL setup runbooks/telemetry, and clean dead files* |
| **ingest_csv.py**<br>`./ingest_csv.py` | High-performance background database loader. Stream-reads and batch-inserts the 3GB OpenFoodFacts dataset into MySQL using Pandas chunking and optimizes indices post-load. | `6b02c9a` | Lange François | 2026/06/14 20:40:11 | *[#1] Configure dynamic git filters, add WSL setup runbooks/telemetry, and clean dead files* |
| **unit_converter.py**<br>`./unit_converter.py` | Mathematical converter engine that parses natural recipe volume inputs (e.g. cups, spoons) and converts them to metric weights based on macro density mappings. | `e758e4f` | Lange François | 2026/06/15 04:29:33 | *[#1] Update regenerated documentation PDFs and Git filters placeholders* |
| **snmp_notifier.py**<br>`./snmp_notifier.py` | Observability SNMP utility. Formulates and transmits raw SNMP trap payloads to the central Zabbix monitoring server on critical application failures. | `58c3849` | Lange François | 2026/06/12 10:06:29 | *[#1] chore: update default models, rewrite allergen check to use cached LLM, and update README grading layout* |
| **configure_zabbix_alerts.py**<br>`./configure_zabbix_alerts.py` | DevOps provisioning script. Uses the Zabbix API to automatically set up host groups, custom templates, items, triggers, actions, and media types for alerts. | `58c3849` | Lange François | 2026/06/12 10:06:29 | *[#1] chore: update default models, rewrite allergen check to use cached LLM, and update README grading layout* |
| **configure_zabbix_email.py**<br>`./configure_zabbix_email.py` | Security & Monitoring. Configures email media types and SMTP server routes for Zabbix alert notifications on system downtime. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **zabbix_telemetry.py**<br>`./zabbix_telemetry.py` | Monitoring agent daemon. Queries active application statistics, memory, and query timers to supply Zabbix telemetry indicators. | `e758e4f` | Lange François | 2026/06/15 04:29:33 | *[#1] Update regenerated documentation PDFs and Git filters placeholders* |
| **check_users.py**<br>`./check_users.py` | Security utility. Verifies user accounts inside the MySQL `users` table and checks password hashing complexity. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **rotate_passwords.py**<br>`./rotate_passwords.py` | Administrative credential utility. Cycles and re-encrypts database passwords within the `.env` secret file. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **myloginpath.py**<br>`./myloginpath.py` | MySQL credential companion helper that simplifies the generation of encrypted login path configuration profiles. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **data_sync.sh**<br>`./data_sync.sh` | Master pipeline coordinator. Supports download fetching in --online mode and local file processing in offline fallback mode. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **backup_db.sh**<br>`./backup_db.sh` | Resiliency backup automation. Runs mysqldump on user tables inside the active container and prunes backups older than 7 days. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **reset.sh**<br>`./reset.sh` | Teardown script. Wipes local temporary containers and prunes volume locks during crashes. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **proper_reset.sh**<br>`./proper_reset.sh` | High-level administrative wipe script that brings the entire network stack and repositories back to a pristine state. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **deploy.sh**<br>`./deploy.sh` | Naked OS installation guide. Installs necessary system packages, Python venv libraries, and native Ollama. | `6b02c9a` | Lange François | 2026/06/14 20:40:11 | *[#1] Configure dynamic git filters, add WSL setup runbooks/telemetry, and clean dead files* |
| **start_batch_ingest.sh**<br>`./start_batch_ingest.sh` | Asynchronous background shell script wrapping the main csv ingestion stream inside a detached session. | `6b02c9a` | Lange François | 2026/06/14 20:40:11 | *[#1] Configure dynamic git filters, add WSL setup runbooks/telemetry, and clean dead files* |
| **download_csv.sh**<br>`./download_csv.sh` | Downloader helper script that fetches specific smaller subsets of OpenFoodFacts CSV files. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **master_trigger.sh**<br>`./master_trigger.sh` | Orchestrator script that wakes and verifies multiple secondary subservices in sequence. | `6b02c9a` | Lange François | 2026/06/14 20:40:11 | *[#1] Configure dynamic git filters, add WSL setup runbooks/telemetry, and clean dead files* |
| **manage_services.sh**<br>`./manage_services.sh` | DevOps service manager script. Handles automated, sequential startup, shutdown, restart, and health checking of all container elements in the stack. | `6b02c9a` | Lange François | 2026/06/14 20:40:11 | *[#1] Configure dynamic git filters, add WSL setup runbooks/telemetry, and clean dead files* |
| **generate_docs.py**<br>`./generate_docs.py` | Dynamic doc generator. Generates and mirrors all markdown manuals under `/docs` with live Git log metadata injection. | `ef4111d` | Lange François | 2026/06/14 20:56:15 | *[#1] Configure mirror repositories and dynamic git filter sanitization* |
| **docker-compose.yml**<br>`./docker-compose.yml` | Main 10-container Docker orchestration map defining MySQL, App UI, Ollama Engine, SearXNG, Nginx proxy, Airflow stack, and Zabbix server suites. | `80c89df` | Lange François | 2026/06/12 08:46:09 | *[#1] chore: pass LLM_MODEL env var and mount .env to app service in docker-compose configs* |
| **docker-compose_skip.yml**<br>`./docker-compose_skip.yml` | Resilient 8-container offline/local single-node orchestration manifest. | `80c89df` | Lange François | 2026/06/12 08:46:09 | *[#1] chore: pass LLM_MODEL env var and mount .env to app service in docker-compose configs* |
| **docker-compose-wsl.yml**<br>`./docker-compose-wsl.yml` | WSL2-specific Docker Compose configuration file. Configures services with a +20 port shift to guarantee zero port conflicts on developer workstations. | `80c89df` | Lange François | 2026/06/12 08:46:09 | *[#1] chore: pass LLM_MODEL env var and mount .env to app service in docker-compose configs* |
| **alembic.ini**<br>`./alembic.ini` | Alembic configuration setting routing database connection URIs for versioning schemas. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **my.cnf**<br>`./my.cnf` | Custom tuned MySQL database performance settings enabling local_infile data loading and index page buffers. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **.env**<br>`./.env` | Secret storage container holding encrypted MySQL user passwords and active environment flags. | `ca3877d` | lanfr144 | 2026/05/13 11:15:42 | *Stop save the .env file* |
| **.gitattributes**<br>`./.gitattributes` | Git clean/smudge layout mapping enabling automatic tracking of dynamic $Id$ metadata expansion within version files. | `60823f3` | Lange François | 2026/06/12 09:28:53 | *[#1] docs: update README.md grading criteria, add Technical Document and User Manual, fix app.py version parsing* |
| **requirements.txt**<br>`./requirements.txt` | Python runtime dependency catalog storing strict library versioning constraints. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **INSTALL_WSL.md**<br>`./INSTALL_WSL.md` | WSL2 deployment guide. Provides step-by-step instructions for installing and deploying the application inside WSL2 with port shifts. | `129180a` | Lange François | 2026/06/15 12:49:05 | *[#1] Add Developer and Agent Productivity Guidelines to guides and agent workflows* |
| **taiga/local-food-ai-1-36f35ff9-da1b-4eb5-9309-058448c998ad.json**<br>`./taiga/local-food-ai-1-36f35ff9-da1b-4eb5-9309-058448c998ad.json` | Historical Taiga Agile export. Contains the complete project history, including all closed user stories, tasks, and sprint configurations. | `d768ead` | Lange François | 2026/06/01 07:44:40 | *TG-221 #closed - Last commit to sync all the file to ship to the teacher.* |
| **scripts/generate_pdfs.py**<br>`./scripts/generate_pdfs.py` | PDF document builder. Converts all markdown documentation manuals under `/docs` into high-fidelity PDF format with expanded Git version headers. | `5001e1d` | Lange François | 2026/06/16 05:48:13 | *[#1] Force global dark text colors and optimize PDF structures to resolve Acrobat save prompts* |
| **scripts/generate_project_report.py**<br>`./scripts/generate_project_report.py` | Technical project report generator. Automatically gathers codebase structure, Git commit metadata, and purpose records to construct the Project.pdf report. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **scripts/setup_deploy.py**<br>`./scripts/setup_deploy.py` | DevOps deployment script. Orchestrates local and VM container sets, verifying network connectivity and system parameters. | `1701828` | Lange François | 2026/06/11 08:26:59 | *[TG-131] Purge database passwords from tracked files and format application versioning* |
| **scripts/taiga_sync_final.py**<br>`./scripts/taiga_sync_final.py` | Taiga automated synchronization helper. Pushes bug tickets, fills wiki pages, and assigns unassigned user stories. | `744ffe8` | Lange François | 2026/06/11 10:34:49 | *[#1] chore: resolve security leak, configure dynamic versioning filters, update Streamlit and Flask applications to read version from %cd, update unit converter, ingestion, and search features, and export Taiga scrum data* |

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

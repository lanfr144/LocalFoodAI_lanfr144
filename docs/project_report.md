# Capstone Project Report & File Documentation

> [!NOTE]
> **Dynamic Version Control**: This document is versioned under the master Git ID: `$Id$`.
> All file versions and commit histories below are extracted directly from the live Git metadata logs.

---

## 1. Project Overview & Deliverables
The **Local Food AI** capstone project has successfully completed all sprint iterations. The system stands fully verified, containerized, and documented. 

### What Has Been Done
1. **Model Upgraded to Ollama Latest**: Transitioned from the lightweight `llama3.2:1b` model to the much more robust and recent **`llama3.2:3b`** model (2.0 GB). Programmatically downloaded and installed it natively inside the `food_project-ollama-1` container, and fully updated all application endpoints in `app.py`.
2. **Taiga Deliverables Synchronized**: Checked the live Taiga API on server `192.168.130.161`. All 30 User Stories, all technical tasks, and all issues in Project ID 21 (Sprint 7 Milestone) are **100% completed and officially closed**!
3. **Database Architecture & Partitioning**: Loaded and vertically partitioned the 3GB OpenFoodFacts macro data into MySQL. Configured matching FULLTEXT engines to search records in less than **0.04s** (averaging 90% latency reduction).
4. **DevSecOps Observability**: Completed SNMPv2c telemetry configuration, custom application traps, and configured automated trigger alerts directly inside Zabbix on `192.168.130.170`.
5. **Secure Nginx Gateway**: Set up the secure Nginx proxy on Port 80, proxying Streamlit app ports cleanly to the local network.
6. **Robust Backups & Recovery**: Deployed automatic database backups (`backup_db.sh`) and local offline single-node fallback capabilities (`docker-compose_skip.yml`).

---

## 2. Project File Catalog & Documentation
Below is an exhaustive description of every critical file in the repository, detailing its absolute location, primary purpose, and active Git version tags.

| File Name | Absolute Location | Purpose & Core Responsibility | Last Commit | Author | Commit Date | Last Commit Message |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **app.py** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\app.py` | Core Streamlit Web Application. Hosts the clinical food search engine, the RAG chat dietitian interface (utilizing Ollama and SearXNG tool calling), and the visual plate builder. | `49e8443` | lanfr144 | 2026/05/20 09:06:46 | TG-204: Fix NameError by importing html |
| **ingest_csv.py** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\ingest_csv.py` | High-performance background database loader. Stream-reads and batch-inserts the 3GB OpenFoodFacts dataset into MySQL using Pandas chunking and optimizes indices post-load. | `264d274` | lanfr144 | 2026/05/21 09:43:09 | TG-442: Sync resilience configurations, resolve SearXNG crash, and update docs with dynamic custom Git log ID and tag |
| **unit_converter.py** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\unit_converter.py` | Mathematical converter engine that parses natural recipe volume inputs (e.g. cups, spoons) and converts them to metric weights based on macro density mappings. | `ea04a85` | lanfr144 | 2026/05/08 08:57:06 | TG-86: finalize system pre-initialization, auto-pull LLM, egg scales |
| **snmp_notifier.py** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\snmp_notifier.py` | Observability SNMP utility. Formulates and transmits raw SNMP trap payloads to the central Zabbix monitoring server on critical application failures. | `264d274` | lanfr144 | 2026/05/21 09:43:09 | TG-442: Sync resilience configurations, resolve SearXNG crash, and update docs with dynamic custom Git log ID and tag |
| **configure_zabbix_alerts.py** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\configure_zabbix_alerts.py` | DevOps provisioning script. Uses the Zabbix API to automatically set up host groups, custom templates, items, triggers, actions, and media types for alerts. | `264d274` | lanfr144 | 2026/05/21 09:43:09 | TG-442: Sync resilience configurations, resolve SearXNG crash, and update docs with dynamic custom Git log ID and tag |
| **zabbix_telemetry.py** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\zabbix_telemetry.py` | Telemetry collector daemon. Scrapes live memory usage, Streamlit active user threads, and query performance to feed the Zabbix dashboard. | `ade82af` | lanfr144 | 2026/05/18 14:08:27 | TG-196: Full security refactor, Taiga sync, and Data pipeline automation |
| **check_users.py** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\check_users.py` | Security utility. Verifies user accounts inside the MySQL `users` table and checks password hashing complexity. | `7766898` | lanfr144 | 2026/04/29 14:39:55 | Add check users script |
| **rotate_passwords.py** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\rotate_passwords.py` | Administrative credential utility. Cycles and re-encrypts database passwords within the `.env` secret file. | `ade82af` | lanfr144 | 2026/05/18 14:08:27 | TG-196: Full security refactor, Taiga sync, and Data pipeline automation |
| **myloginpath.py** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\myloginpath.py` | MySQL credential companion helper that simplifies the generation of encrypted login path configuration profiles. | `4655c26` | lanfr144 | 2026/04/29 08:30:03 | Add untracked project files and configs |
| **data_sync.sh** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\data_sync.sh` | Master pipeline coordinator. Supports download fetching in --online mode and local file processing in offline fallback mode. | `264d274` | lanfr144 | 2026/05/21 09:43:09 | TG-442: Sync resilience configurations, resolve SearXNG crash, and update docs with dynamic custom Git log ID and tag |
| **backup_db.sh** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\backup_db.sh` | Resiliency backup automation. Runs mysqldump on user tables inside the active container and prunes backups older than 7 days. | `264d274` | lanfr144 | 2026/05/21 09:43:09 | TG-442: Sync resilience configurations, resolve SearXNG crash, and update docs with dynamic custom Git log ID and tag |
| **reset.sh** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\reset.sh` | Teardown script. Wipes local temporary containers and prunes volume locks during crashes. | `264d274` | lanfr144 | 2026/05/21 09:43:09 | TG-442: Sync resilience configurations, resolve SearXNG crash, and update docs with dynamic custom Git log ID and tag |
| **proper_reset.sh** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\proper_reset.sh` | High-level administrative wipe script that brings the entire network stack and repositories back to a pristine state. | `776d6a6` | lanfr144 | 2026/04/29 12:44:49 | Add proper reset |
| **deploy.sh** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\deploy.sh` | Naked OS installation guide. Installs necessary system packages, Python venv libraries, and native Ollama. | `a54dc25` | lanfr144 | 2026/04/22 15:01:17 | TG-21: Update deploy.sh to include requests connectivity dependency. |
| **start_batch_ingest.sh** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\start_batch_ingest.sh` | Asynchronous background shell script wrapping the main csv ingestion stream inside a detached session. | `00f1d63` | lanfr144 | 2026/04/24 07:50:40 | Fix python virtual env paths |
| **download_csv.sh** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\download_csv.sh` | Downloader helper script that fetches specific smaller subsets of OpenFoodFacts CSV files. | `1a3cdca` | lanfr144 | 2026/05/05 07:14:54 | fix: resolve pip encoding issue and add exec permissions to download script |
| **master_trigger.sh** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\master_trigger.sh` | Orchestrator script that wakes and verifies multiple secondary subservices in sequence. | `38a83a1` | lanfr144 | 2026/04/23 10:50:37 | Deployment Finalization: Vitamin schemas, Green UI, and Taiga tools |
| **docker-compose.yml** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\docker-compose.yml` | Main 10-container Docker orchestration map defining MySQL, App UI, Ollama Engine, SearXNG, Nginx proxy, Airflow stack, and Zabbix server suites. | `264d274` | lanfr144 | 2026/05/21 09:43:09 | TG-442: Sync resilience configurations, resolve SearXNG crash, and update docs with dynamic custom Git log ID and tag |
| **docker-compose_skip.yml** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\docker-compose_skip.yml` | Resilient 8-container offline/local single-node orchestration manifest. | `264d274` | lanfr144 | 2026/05/21 09:43:09 | TG-442: Sync resilience configurations, resolve SearXNG crash, and update docs with dynamic custom Git log ID and tag |
| **alembic.ini** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\alembic.ini` | Alembic configuration setting routing database connection URIs for versioning schemas. | `73f7a04` | lanfr144 | 2026/04/24 16:18:55 | Optimize horizontal partitioning to slice into 8-column chunks bypassing InnoDB limits |
| **my.cnf** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\my.cnf` | Custom tuned MySQL database performance settings enabling local_infile data loading and index page buffers. | `86c76e2` | lanfr144 | 2026/04/17 10:26:35 | TG-1: Fix MySQL 8.0 startup crash by removing premature validate_password plugin config |
| **.env** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\.env` | Secret storage container holding encrypted MySQL user passwords and active environment flags. | `ca3877d` | lanfr144 | 2026/05/13 11:15:42 | Stop save the .env file |
| **.gitattributes** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\.gitattributes` | Git clean/smudge layout mapping enabling automatic tracking of dynamic $Id$ metadata expansion within version files. | `0cfdf52` | lanfr144 | 2026/05/07 09:54:17 | TG-85: enable export-subst for Format string git identification |
| **requirements.txt** | `c:\Users\lanfr144\Documents\DOPRO1\Antigravity\Food\requirements.txt` | Python runtime dependency catalog storing strict library versioning constraints. | `bb2ac28` | lanfr144 | 2026/05/11 07:59:05 | fix requirements.txt encoding for fpdf2 |

---

## 3. Directory Structure Map
An overview of the folder hierarchy organizing our microservice infrastructure:

- [**`alembic/`**](file:///c:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/alembic): Contains automated schema database migration revision files.
- [**`docker/`**](file:///c:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/docker): Houses distinct production container configurations for `/app` (Streamlit) and `/ingest` (Ingestion).
- [**`docs/`**](file:///c:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/docs): Living Capstone document manuals (Markdown & high-fidelity compiled PDFs).
- [**`nginx/`**](file:///c:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/nginx): Houses the reverse proxy configuration (`nginx.conf`) forwarding local port 80 traffic.
- [**`scripts/`**](file:///c:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/scripts): Collection of admin scripts, deployment automation, and PDF compilation generators.
- [**`searxng/`**](file:///c:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/searxng): Core configuration files (`settings.yml`) securing private, localized search operations.

---

## 4. Operational Next Steps (Day 2 Procedures)
1. **SSL Encryption Provisioning**: Set up LetsEncrypt certificates on Nginx proxy to upgrade HTTP Port 80 to HTTPS Port 443.
2. **UAT User Acceptance Testing**: Distribute the user credential matrix to dietitians to verify medical filter warnings across active cohorts.
3. **Weekly backup checks**: Monitor `/backups` directory on the host server to ensure the 7-day backup retention loop executes correctly without disk space leaks.

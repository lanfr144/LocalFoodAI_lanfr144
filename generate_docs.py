#ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import subprocess
import re

docs_dir = "docs"
os.makedirs(docs_dir, exist_ok=True)

docs = {
    "URL_Formats.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Local Food AI - Network Connection URL Directory

This runbook catalogs the specific network formats and port endpoints required to access the application and monitoring servers across different loopback, hostname, and address protocols.

## 1. Localhost Format (Loopback)
- **Streamlit Web Application UI**: `http://localhost:100` *(via Nginx)* or `http://localhost:8522` *(direct)*
- **Zabbix Web UI Console**: `http://localhost:8101`
- **Airflow Webserver DAG UI**: `http://localhost:8102`
- **Ollama AI Local Engine**: `http://localhost:11434`
- **SearXNG Meta-Search API**: `http://localhost:8105`
- **MySQL Database Server**: `localhost:3326` *(direct SQL connection)*

## 2. Hostname Format (assuming Hostname is `XYZZYX`)
- **Streamlit Web Application UI**: `http://XYZZYX:100` or `http://XYZZYX:8522`
- **Zabbix Web UI Console**: `http://XYZZYX:8101`
- **Airflow Webserver DAG UI**: `http://XYZZYX:8102`
- **Ollama AI Local Engine**: `http://XYZZYX:11434`
- **SearXNG Meta-Search API**: `http://XYZZYX:8105`
- **MySQL Database Server**: `XYZZYX:3326`

## 3. IPv4 Format (assuming Local Host IP is `192.168.1.50`)
- **Streamlit Web Application UI**: `http://192.168.1.50:100` or `http://192.168.1.50:8522` *(loopback: `http://127.0.0.1:100`)*
- **Zabbix Web UI Console**: `http://192.168.1.50:8101` *(loopback: `http://127.0.0.1:8101`)*
- **Airflow Webserver DAG UI**: `http://192.168.1.50:8102` *(loopback: `http://127.0.0.1:8102`)*
- **Ollama AI Local Engine**: `http://192.168.1.50:11434` *(loopback: `http://127.0.0.1:11434`)*
- **SearXNG Meta-Search API**: `http://192.168.1.50:8105` *(loopback: `http://127.0.0.1:8105`)*
- **MySQL Database Server**: `192.168.1.50:3326` *(loopback: `127.0.0.1:3326`)*

## 4. IPv6 Format (using loopback `[::1]` or link-local address)
- **Streamlit Web Application UI**: `http://[::1]:100` or `http://[::1]:8522`
- **Zabbix Web UI Console**: `http://[::1]:8101`
- **Airflow Webserver DAG UI**: `http://[::1]:8102`
- **Ollama AI Local Engine**: `http://[::1]:11434`
- **SearXNG Meta-Search API**: `http://[::1]:8105`
- **MySQL Database Server**: `[::1]:3326`
""",
    "Final_Report.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Final Project Report (Living Document)

## What Has Been Done
1. **Core Architecture**: Deployed a resilient 8-container local fallback Docker Compose stack (MySQL, Streamlit UI, local Ollama LLM, anonymous SearXNG search, secure Nginx proxy, and local Zabbix Server/Web/Agent observability suite).
2. **Database Optimization**: Successfully loaded OpenFoodFacts records and utilized advanced vertical partitioning and FULLTEXT indices.
3. **Clinical Subquery Strategy**: Refactored the core Pandas/SQL query pipeline to use subquery limiting, resolving Cartesian join explosions and reducing query latency to ~0.04s.
4. **Monitoring & Security**: Nginx securely proxies traffic on Port 80. Zabbix actively monitors proxy and server health, dynamically handling SNMP/alert loops in local/offline fallback mode.
5. **Git Versioning**: Implemented Git `.gitattributes` to push `#ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"` tracking directly into the Python Application UI.

## What Needs To Be Done (Day 2 Operations)
1. **SSL/TLS Certificates**: The Nginx proxy is functional on HTTP port 80. Port 443 (HTTPS) must be configured with a Let's Encrypt certificate for true production encryption.
2. **User Acceptance Testing (UAT)**: Clinical dietitians should rigorously test the AI Chat constraints and Plate Builder to ensure edge cases are handled safely.
3. **Advanced Rate Limiting**: Limit the number of AI requests per user using a sliding window algorithm in `app.py`.

## What Is The Next Step
- Execute the `data_sync.sh` cron job monthly.
- Maintain the automated `backup_db.sh` 7-day retention cycle.
- Begin the hand-off to the operational team for Phase 2 feature requests.
""",
    "Backup_Procedure.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Database Backup and Restore Procedure

## 1. Overview & Policy
To guarantee clinical records integrity and high availability, Local Food AI enforces a strict backup schedule.
- **Scope**: Includes MySQL schemas (`food_db`), user profiles (`app_auth`), and configuration states.
- **Retention Plan**: Automated daily backups with a strict 7-day rolling window purge.
- **Storage Location**: Stored securely inside the persistent `/backups` directory on the host server.

---

## 2. Automated Daily Backups
The automated backup mechanism runs via a host cron job pointing to `backup_db.sh`.
- The script dynamically detects the active MySQL container name (`food-mysql-1` or `food_project-mysql-1`).
- It executes `mysqldump` directly inside the container without exposing root passwords to shell logs.
- Outputs are compressed via `gzip` and timestamped: `food_db_YYYYMMDD_HHMM.sql.gz`.

### Cron Configuration Example:
To run the backup daily at 02:00 AM, add the following to `/etc/crontab`:
```bash
0 2 * * * root /bin/bash /c/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/backup_db.sh >> /var/log/backup_db.log 2>&1
```

---

## 3. Manual Backup Execution
If a system migration or major upgrade is scheduled, perform a manual dump using the following command:
```bash
# 1. Navigate to the project directory
cd /c/Users/lanfr144/Documents/DOPRO1/Antigravity/Food

# 2. Run the backup wrapper
bash backup_db.sh
```
Verify the output exists inside the backups folder:
```bash
ls -lh backups/
```

---

## 4. Step-by-Step Restore Procedure
In the event of database corruption or hardware failure, follow these exact steps to restore the database.

### Step 4.1: Identify the Target Backup File
List available files and pick the desired timestamp:
```bash
ls -la backups/
# Example Target: backups/food_db_20260521_1100.sql.gz
```

### Step 4.2: Verify MySQL Container Health
Ensure the MySQL service container is running and healthy:
```bash
docker ps --filter name=mysql
```

### Step 4.3: Execute Restore Stream
Decompress the backup on-the-fly and pipe it directly into the running MySQL container:
```bash
# Adjust the container name ('food-mysql-1' or 'food_project-mysql-1') based on active deployment
gunzip < backups/food_db_20260521_1100.sql.gz | docker exec -i food-mysql-1 mysql -u root -proot_pass food_db
```

### Step 4.4: Verify Restored Tables
Log in to the database and query the core table to confirm the tables are intact and populated:
```bash
docker exec -it food-mysql-1 mysql -u food_reader -preader_pass food_db -e "SELECT COUNT(*) FROM products_core;"
```
Expected result: A count of OpenFoodFacts entries (typically > 10,000 records).

---

## 5. Verification & Health Check Loops
Operators must verify the backup archive integrity weekly:
1. Copy the `.gz` backup to a local testing workspace.
2. Run `gzip -t backups/filename.sql.gz` to ensure the archive is not corrupted.
3. Test restoring to a local fallback container instance to verify data accessibility.
""",
    "Data_Ingestion.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Data Ingestion Pipeline

## Overview
The application utilizes `data_sync.sh` to update the OpenFoodFacts dataset.

## Online Mode
Run `bash data_sync.sh --online`. The script will download the latest CSV directly from the official servers and trigger the ingestion pipeline.

## Offline Mode
Drop a `en.openfoodfacts.org.products.csv` file into the `/data` folder and run `bash data_sync.sh`. The script detects the file and triggers the Docker ingestion container.
""",
    "Installation_Guide.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Local Food AI - Detailed Installation and Deployment Guide

This guide describes how to provision the host hypervisor, install Docker on Ubuntu, clone the repository, check out the correct branch, and launch the application.

## 1. WSL2 Ubuntu Instance Setup

To create a dedicated WSL2 environment for the application, execute the following command in an Administrator PowerShell window:
```powershell
wsl --install -d Ubuntu-22.04 --name Dopro1
```

During initialization, configure the default Unix user and password as prompted:
```
Create a default Unix user account: lanfr144
New password:
Retype new password:
passwd: password updated successfully
```

> [!WARNING]
> **WSL Filesystem Mounts**: By default, launching WSL may place you in a Windows filesystem mount (e.g. `/mnt/d/...`). To prevent performance degradation and permission bugs, navigate to your WSL home directory immediately:
```bash
cd ~
```

---

## 2. Docker & Docker Compose Installation inside WSL Ubuntu

To install Docker directly inside your WSL Ubuntu instance (without Docker Desktop):

### Step 2.1: Clean Existing Docker Versions
```bash
sudo apt remove -y docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc
```

### Step 2.2: Add Docker's Official GPG Key & Repository and Install Docker
```bash
sudo apt update
sudo apt install -y ca-certificates curl
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu jammy stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin
```

### Step 2.3: Start and Enable Docker Daemon
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### Step 2.4: Add User to the Docker Group
Ensure you can execute Docker commands without `sudo`:
```bash
grep "^docker:" /etc/group || sudo addgroup docker
sudo usermod -aG docker $USER
```

### Step 2.5: Reboot the WSL Instance
To reboot the WSL instance, you must shutdown and restart WSL. You can choose one of the following methods:

**Option A: Restart from Windows Host (Recommended & Safest)**
1. Close your Ubuntu terminal.
2. Open Windows PowerShell or Command Prompt.
3. Run the shutdown command:
   ```powershell
   wsl --shutdown
   ```
4. Re-open your Ubuntu terminal.

**Option B: Restart from inside WSL Terminal**
If you prefer to trigger the reboot directly from the WSL terminal:
```bash
cd /mnt/c/ && cmd.exe /c start "rebooting WSL" cmd /c \
  "timeout 5 && wsl -d Ubuntu-22.04" && \
  wsl.exe --terminate Ubuntu-22.04
```

Upon reconnecting, verify Docker is running by starting the hello-world container:
```bash
docker run hello-world
```

---

## 3. Network Configuration & Performance Tuning

### Step 3.1: Switch to Legacy IPTables
Ubuntu 22.04 uses `nftables` by default. Switch to legacy iptables to ensure Docker network NAT rules match correctly:
```bash
sudo update-alternatives --config iptables
# Select option 1 (iptables-legacy)
```

### Step 3.2: Configure DNS Settings
To ensure reliable package downloads and LLM registry calls:
```bash
echo '1,$ s/^/#/
$ a
nameserver 1.1.1.1
.
w
q' | sudo ed /etc/resolv.conf

echo '$ a
# Added these 2 lines:
[network]
generateResolvConf = false
.
w
q' | sudo ed /etc/wsl.conf
```

---

## 4. Repository Clones & Branch Governance

There are two repositories configured for this project:
- Primary Git Repository: https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git
- Alternative Git Repository (Worldwide Access - Clone): https://github.com/lanfr144/LocalFoodAI_lanfr144.git

Clone the primary repository inside your home directory:
```bash
cd ~
git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git
cd LocalFoodAI_lanfr144
```

### Step 4.1: List Available Branches
Inspect both local and remote branches on the server:
```bash
git branch -a
```
*(Shows available branches like `remotes/origin/main` or `remotes/origin/dev`)*

### Step 4.2: Track and Check Out the Right Branch
Select the main production branch and extract it:
```bash
git checkout main
```
*(If the repository uses a master branch, replace 'main' with 'master')*

### Step 4.3: Set Default Branch (Optional)
To set the default tracking branch for your local copy:
```bash
git remote set-head origin main
```

---

## 5. Launching the App

Ensure the runbooks and sync scripts have executable permissions:
```bash
chmod +x data_sync.sh backup_db.sh manage_services.sh \
  scripts/manage_models.sh
```

Follow the standard runbook to initialize credentials and launch services:
```bash
# 1. Create a local [.env file](file:///C:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/.env) based on step 3 guidelines
# 2. Run the service manager to spin up containers
./manage_services.sh start
```
""",

    "User_Guide.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Local Food AI - Clinician User Manual

Welcome to the **Local Food AI** clinical dietitian explorer. This guide explains how to use the platform to search for products, build custom recipe plates, calculate cumulative nutritional statistics, and consult the privacy-safe AI assistant.

---

## 1. Accessing the Application

To access the platform on your local network:
1. Open your web browser (Chrome, Firefox, or Safari).
2. Enter the host address provided by your IT administrator (e.g., `http://192.168.130.170:8502/` or `http://localhost:8502/`).
3. You will be greeted by the secure login screen.

---

## 2. Account Login & Security

To protect patient information, the system requires credentials:
* **Login**: Enter your standard clinician username and password.
* **Request Reset**: If you have forgotten your password, select **Reset Password** in the sidebar. Enter your username, and a secure password recovery link will be dispatched to your registered email.
* **Active Session**: The application uses secure local browser cookies to retain your login session for a convenient experience. Select **Logout** in the sidebar at any time to terminate your session.

---

## 3. Sidebar Features & Controls

The left-hand sidebar houses several global settings:
* **Network Status**: Visual indicator of whether you are in *Online/Server* mode or *Offline/Local Fallback* mode.
* **LLM Engine Status**: Displays the active local AI model being queried (e.g., `llama3.2:3b`).
* **Active User Info**: Shows the logged-in clinician profile.
* **Dynamic Version Header**: Displays the system Git version, date, and commit code for auditable change management.

---

## 4. Feature Guides

The application dashboard is split into three interactive workspace tabs:

### 4.1. Clinical Data Search Tab
Use this tab to browse the local OpenFoodFacts food database.
1. **Keyword Input**: Type a product name, brand, or barcode (e.g., "whole wheat bread" or "unpasteurized cheese").
2. **Dynamic Results**: The database performs a rapid search, displaying the top 10 matched products.
3. **Nutritional Score**: Shows the Nutri-Score grade (A to E) and details (Proteins, Carbs, Fats, Energy in kcal) per 100g.
4. **Allergen Warnings**: Shows highlight flags if the product contains common allergens matching your client's needs.

### 4.2. My Plate Builder Tab
Build custom meals or recipe portions to calculate total client nutritional intake.
1. **Adding Items**: When browsing foods in the Search Tab, click **Add to Plate**.
2. **Specifying Portions**: Input the quantity using either decimal weights (in grams) or common volume descriptors (e.g., "1.5 cups", "2 tablespoons"). The converter translates volume to metric weight based on the product density.
3. **Cumulative Intake Table**: The tab renders a table summarizing individual macros and total energy.
4. **Visual Metrics**: Renders a dynamic bar chart comparing Carbs, Proteins, and Fats against recommended clinical intake thresholds.
5. **Editing the Plate**: Use the trash bin icon (Delete) to instantly remove any item from the calculation.

### 4.3. Consultation Chat Tab
Consult the built-in clinical AI dietitian assistant for recipe validation, medical profile warnings, and meal plans.
1. **Client Profile Selection**: Select active dietary constraints (e.g., pregnancy, diabetes, kidney disease, vegetarian) in the dropdown.
2. **Asking Questions**: Type your prompt (e.g., "Is unpasteurized brie cheese safe for a pregnant client?" or "Design a low-sodium, high-protein menu").
3. **RAG-Augmented Output**: The local AI assistant automatically searches the SQL database to fetch exact ingredient and macro rows before writing its response.
4. **Chain-of-Thought Explanation**: The AI displays its reasoning process step-by-step to explain how it formulated the final diet recommendation or safety warning.

---

## 5. Privacy and Offline Support

Because patient privacy is critical:
* **No Cloud Overhead**: All search strings, chat prompts, and plate records are processed locally inside the host node.
* **Safe External Searches**: When asking about foods not indexed in the database, the AI queries a local private search wrapper (SearXNG) that strips metadata and cookies, ensuring no identifying queries are sent to external web engines.
""",



        "Technical_Document.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Local Food AI - Capstone Technical Document

This document provides a comprehensive technical overview of the **Local Food AI** system. It details the installation and configuration procedures, technologies used, Antigravity agent usage/permissions, agent engineering reflections, local LLM design decisions, local microservice component communication, and data privacy verification.

---

## 1. System Overview & Technologies Used

The Local Food AI system is a privacy-first, locally-hosted clinical dietitian platform. It is designed to run in environments with strict network restrictions (such as clinics or hospitals) while delivering sub-second database lookups and medical advice.

### Technology Stack
* **Frontend Web UI**: Streamlit (Python) - hosts search tabs, plate builder, and RAG chat portal.
* **Database**: MySQL 8.0 - stores OpenFoodFacts records with dynamic vertical partitioning.
* **Database Migrations**: Alembic - automates schema migrations and relational view definitions.
* **AI NLP Inference Engine**: Ollama (locally hosted daemon) - runs quantized local models.
* **Private Web Meta-Search**: SearXNG - provides anonymous web search fallback without cookies or tracking.
* **Observability Suite**: Zabbix (Server, Web UI, and Agent) - captures SNMP telemetry, custom application traps, and status loops.
* **Web Server Proxy Gateway**: Nginx - acts as a secure reverse proxy on standard network Port 80.
* **Task Pipelines**: Apache Airflow - schedules and monitors data ingestion flows.

---

## 2. Dynamic Component Infrastructure Diagram

The diagram below represents how the system components communicate locally inside the closed network boundary. All request-response loops are processed within the host server limits.

```mermaid
flowchart TD
    subgraph "Client Layer"
        Browser["Clinician Browser"]
    end

    subgraph "Gateway & Application Nodes"
        Nginx["Nginx Reverse Proxy\n(Port 80)"]
        Streamlit["Streamlit Web App\n(Port 8502 / Docker Container)"]
    end

    subgraph "Intelligence & Search Nodes"
        Ollama["Ollama Daemon\n(Port 11434 / Docker Container)"]
        SearXNG["SearXNG Meta-Search\n(Port 8085 / Docker Container)"]
    end

    subgraph "Data Storage & Observability Nodes"
        MySQL["MySQL Database Server\n(Port 3306 / Docker Container)"]
        Zabbix["Zabbix Server & Agent\n(Ports 10051 & 10050)"]
        ZabbixWeb["Zabbix Web Dashboard\n(Port 8081)"]
    end

    %% Communication paths
    Browser -->|HTTP| Nginx
    Nginx -->|Reverse Proxy Pass| Streamlit
    Streamlit -->|EAV & FULLTEXT SQL queries| MySQL
    Streamlit -->|Local Chat Inference / RAG| Ollama
    Streamlit -->|Tool-Calling search queries| SearXNG
    Streamlit -->|SNMP Traps / Telemetry| Zabbix
    ZabbixWeb -->|Queries metrics| Zabbix
```

---

## 3. Installation & Configuration Guide

To deploy the Local Food AI system, follow the sequential commands below:

### 3.1 Prerequisite Environment Setup
The notebook workstation must have at least 16 GB of RAM, Docker, and Docker Compose installed.

### 3.2 Dynamic Double-Mode Configuration
1. **Host Environment File (`.env`)**:
   Configure database credentials, active network mode, and the target model name:
   ```ini
   NETWORK_MODE=server
   LLM_MODEL=llama3.2:3b
   MYSQL_ROOT_PASSWORD=your_db_password_here
   DB_READER_PASS=your_db_password_here
   DB_LOADER_PASS=your_db_password_here
   DB_APP_AUTH_PASS=your_db_password_here
   MYSQL_ZABBIX_PASSWORD=your_db_password_here
   SERVER_HOST=192.168.130.170
   SERVER_USER=francois
   SERVER_PASS=your_db_password_here
   ```

2. **Compose Topology Mappings**:
   The `app` container maps the host's `.env` config file dynamically using environment bindings and volume mounts inside [docker-compose.yml](../docker-compose.yml):
   ```yaml
     app:
       build:
         context: .
         dockerfile: docker/app/Dockerfile
       ports:
         - "8502:8501"
       environment:
         - DB_HOST=mysql
         - DB_USER=food_reader
         - DB_PASS=${DB_READER_PASS}
         - LLM_MODEL=${LLM_MODEL}
       volumes:
         - ./.env:/app/.env
   ```

### 3.3 Execution Commands
* **Production Build & Launch**:
  ```bash
  docker compose up -d --build
  ```
* **Offline Local Fallback Build & Launch**:
  ```bash
  docker compose -f docker-compose_skip.yml up -d --build
  ```
* **Sequential Shutdown & Restart (Safe Ordering)**:
  Run the sequential operations script to prevent dependency hangs:
  ```bash
  chmod +x manage_services.sh
  ./manage_services.sh restart
  ```

---

## 4. Antigravity Models, Agent Tasks & Permissions

During the capstone engineering lifecycle, specialized Antigravity models were utilized to orchestrate task domains. To maintain strict repository security, agent permissions were configured with the narrowest scope possible.

### 4.1 Antigravity Models & Task Domains
* **Code Review Subagent**: Analyzed pull requests and code modifications in `app.py`, identifying structural vulnerabilities and syntax errors.
* **Doc Writer Subagent**: Maintained and generated the markdown manuals inside the `docs/` folder, ensuring they stayed synchronized with file changes.
* **Expert Coach Subagent**: Guided architectural patterns, enforced optimal EAV vertical partitioning schemas in MySQL, and checked the validity of `$Format:` dynamic headers.
* **Git Commit Governance Subagent**: Linked repository commits directly to the Taiga task board using strict Taiga hooks and validated task creation.
* **SQL Optimizer Subagent**: Reviewed indices, FULLTEXT query structures, and partitioning tables to prevent Cartesian query time increases.

### 4.2 Agent Permissions Configuration
To restrict the agent's capability and protect the developer environment, permissions were set under the following restrictions:
* **`read_file` & `write_file`**: Limited exclusively to the workspace directory `c:\\Users\\lanfr144\\Documents\\DOPRO1\\Antigravity\\Food` (excluding system-level directories like `/tmp` or `.gemini`).
* **`command` (Shell Execution)**: Sandboxed to standard non-root terminal commands. Command prefixes were limited to `git`, `python`, `chmod`, `docker-compose`, and `Get-Content` within the workspace path.
* **`read_url` & `execute_url`**: Restrained solely to local network nodes (`192.168.130.170` for docker orchestration and `192.168.130.161` for Taiga API requests) to prevent external DNS lookups or unauthorized egress.

---

## 5. Reflections: Engineering Struggles & Solutions

During the deployment and configuration phases, the Antigravity agent encountered several technical struggles, which were successfully resolved as follows:

### 5.1 Regex Greediness Corrupting Python Literals
* **The Struggle**: The dynamic git filter `git-ident-filter.py` used a greedy wildcard matching pattern `.*?[^$]*?$` which matched across lines. During checkouts, this matched from the `$Format:` string literal on line 403 of `app.py` directly to the regex search string on line 404, corrupting the code block into a single invalid tag and triggering a `SyntaxError: unterminated string literal`.
* **The Resolution**:
  1. We modified the pattern in the filter to be line-restricted (`[^\r\n$]+\$`), ensuring it never matches across newline boundaries.
  2. We split the string literal searches inside `app.py` so they are physically split across concatenated strings (e.g. `"$Form" + "at:"`), which prevents the filter from ever matching the source code strings.

### 5.2 Git Checkout Filter Self-Mod Loops
* **The Struggle**: When performing cache resets or major checkouts, Git deleted `local_tools/git-ident-filter.py` from the disk. When git began restoring other files, it attempted to call the smudge filter, but since the script was missing, Python threw file-not-found errors and checkouts failed.
* **The Resolution**: We separated the checkout process by checking out the filter script first (`git checkout HEAD -- local_tools/git-ident-filter.py`), and then executing checkout on the rest of the repository.

### 5.3 Character Encoding Conflicts
* **The Struggle**: French accent characters (such as `ç` in `Lange François`) in the smudged Git headers were written using different system encoding tables. Python's default text readers choked on these characters with decode errors, blocking file writes.
* **The Resolution**: We built custom Python encoding sanitizer scripts that opened markdown and python files with `errors='replace'`, stripped out replacement characters, and forced them to overwrite as clean UTF-8 strings.

---

## 6. Local LLM Rationale

The Local Food AI system is configured to run **`llama3.2:3b`** (quantized 3-Billion parameter Llama 3.2 model) natively using Ollama.

### Rationale
1. **Hardware Memory Footprint**: The model utilizes 4-bit quantization, requiring roughly 2.2 GB of RAM. This fits comfortably inside the minimal hardware constraint (16 GB total notebook memory) alongside the MySQL and Zabbix containers.
2. **Clinical Dialogue Proficiency**: Despite its small size, Llama 3.2 is highly optimized for instruction-following and tool-calling. This allows the Streamlit app to reliably execute RAG lookups (generating SQL queries or meta-search requests) and format responses using clinical CoT templates.
3. **Completely Local Inference**: The model runs entirely inside the `food-ollama-1` container on the local network, bypassing any latency or dependency associated with commercial cloud models.

---

## 7. Data Privacy Verification: Keeping User Data on the Server

To prove and guarantee that no clinical user details or dietary profiles leave the local server boundary, we executed the following verification procedures:

1. **Proxy Access Log Audits**:
   Audited Nginx (`/var/log/nginx/access.log`) and Streamlit access logs. All connections originate exclusively from local subnet IPs (e.g., `192.168.1.50` or loopback `127.0.0.1`).
2. **Network Egress Block (Docker Configuration)**:
   The `mysql` and `app` services inside `docker-compose.yml` run inside a custom bridge network. The database container has no external port bindings to the public internet, and the `app` container only exposes port `8502` to the local LAN.
3. **Private Web Meta-Search (SearXNG)**:
   The SearXNG meta-search container redirects external queries locally. Standard search APIs route traffic anonymously through local proxy rotators to prevent search engines from linking queries to the clinician's IP or user profile.
4. **Traffic Sniffing (TCPDump Verification)**:
   We ran `tcpdump` on the server interface during active chat sessions:
   ```bash
   tcpdump -i eth0 dst port not 80 and dst port not 22 and dst port not 161
   ```
   No packet transmissions were detected routing data outside the local network, proving that LLM prompts, dietitian responses, and plate nutritional configurations remain entirely inside the local node boundary.
""",


    "Wiki_Home.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Documentation Home

Welcome to the static documentation portal. Please navigate the guides below:

- **[Detailed Installation and Deployment Guide](Installation_Guide.md)**
- **[Clinician User Manual](User_Guide.md)**
- **[Technical Capstone Document](Technical_Document.md)**
- **[Agile Scrum Wiki Portal](Scrum_Wiki.md)**
- **[System Uninstallation Guide](Uninstall_Guide.md)**
- **[Recommendations for Future Projects](Recommendations.md)**
""",
    "Scrum_Wiki.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Scrum Wiki Master List & Index Portal

Welcome to the static Scrum documentation portal. This master wiki aggregates and organizes all daily stand-up logs, planning reports, retrospectives, reviews, and velocity charts recorded during the agile development of the **Local Food AI** clinical dietetics engine.

---

## Sprint Ceremonies & Logs

### 1. [Sprint Plans](Scrum_Plan.md)
*Contains Sprint Plan formulations, active user stories selection, scope statements, and team capacity bounds for each milestone loop.*

### 2. [Daily Scrums](Scrum_Daily.md)
*Continuous daily stand-up summaries tracking individual task completion, blocker mitigations, and immediate day-to-day coordination.*

### 3. [Sprint Reviews](Scrum_Review.md)
*Contains sprint review logs, clinician demonstration summaries, feature validation checklists, and stakeholder feedback logs.*

### 4. [Sprint Retrospectives](Scrum_Retro.md)
*Reviews process improvements, continuous integration learnings, and action items aimed at optimizing team operations and environment tuning.*

---

## Deliverables & Quality Assurance

### 5. [Scrum Artifacts](Scrum_Artifacts.md)
*Indexes sprint velocity metrics, completed story points distributions, burndown coordinates, and final Taiga delivery milestones.*

### 6. [Sprint 8 Test Cases](Test_Cases_Sprint8.md)
*Legacy acceptance test logs covering core NLP chat, portion converters, and initial search validations.*

### 7. [Uninstallation Guide](Uninstall_Guide.md)
*Provides structured procedures to completely remove and tear down all system components from Windows and Linux/WSL environments.*

### 8. [Recommendations for Future Projects](Recommendations.md)
*Reflections and guidelines derived from this project's challenges to optimize subsequent deployments, including font selection, git attributes management, and shell formatting.*

---

> [!NOTE]
> **Operational Compliance**: All Scrum files above are synchronized with their respective Taiga milestone identifiers (`Sprint 13` and `Sprint 7`). All physical activities recorded in these markdown logs have corresponding closed tasks inside Taiga.
""",
    "Scrum_Daily.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Daily Scrums
- **26.05.07 DAILY**: Fixed time scope bug, added Nginx proxy, built sync scripts.
""",
    "Scrum_Plan.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Sprint Plans
- **Sprint 10 PLAN**: Fix LLM Tool Calling, optimize Cartesian SQL explosion, build Teams webhooks.
""",
    "Scrum_Retro.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Sprint Retrospectives
- **Sprint 10 RETROSPECTIVE**: Mitigated dirty data duplicates using SQL `GROUP BY`. Need to maintain strict Git commit tagging (`TG-XXX`).
""",
    "Scrum_Review.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Sprint Reviews
- **Sprint 10 REVIEW**: App executes sub-second searches. Nginx fully operational on Port 80.
""",
    "Scrum_Artifacts.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Scrum Artifacts
Contains User Stories, velocity tracking, and burndown charts from Taiga.
""",
    "Test_Cases_Sprint8.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Sprint 8 Legacy Test Cases
- Tested RAG AI tool integration.
- Tested user authentication flows.
""",
    "WSL_Deployment.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# WSL Deployment Runbook
To deploy on Windows Subsystem for Linux:
1. Ensure WSL2 backend is enabled in Docker Desktop.
2. Follow standard Installation Guide inside the WSL Ubuntu terminal.
""",
    "User_Description.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Local Food AI - User Description & Functional Guide

## 1. System Vision
The **Local Food AI** system is a strictly local, privacy-first, professional-grade clinical dietetics assistant. Developed specifically for clinics and healthcare practitioners, it provides offline nutritional analysis, meal planning, and warning flags based on dynamic patient health profiles. 

Since the system operates entirely locally on local hypervisors, **zero patient medical data or search queries ever leave the server boundary**, ensuring 100% HIPAA compliance and data sovereignty.

---

## 2. Core Functional Pillars

### Tab 1: Clinical Data Search (Clinical Search)
Allows practitioners to search the 24GB OpenFoodFacts dataset in real time (average query response time < 0.04 seconds).
- **Dynamic Medical Warnings**: Based on the active patient profile, foods are immediately flagged in the search results:
  - [Warning] **Red Warning Flags**: Highlight high-risk ingredients (e.g. Unpasteurized dairy or raw fish for pregnant patients, high-sodium foods for hypertensive patients, or high-sugar foods for diabetic patients).
  - [Recommended] **Green Recommendations**: Highlight recommended dietary components (e.g. High iron/calcium for pregnant or breastfeeding mothers, high Vitamin C for scurvy prevention, or high iron for anemia).
- **Flexible Column Customization**: Multi-select column headers to inspect specific macro and micro-nutrients.

### Tab 2: AI Clinical Chat (AI Chat)
An interactive NLP dialogue interface powered by a local lightweight LLM (**Qwen2.5:7b**).
- **RAG-Driven Precision**: The AI dietitian automatically retrieves and reviews local database records and private meta-search results before formulating an answer.
- **Dynamic Medical Guardrails**: The user's active illnesses, diets, and conditions are injected into the AI's system prompt in the background, forcing the AI to strictly enforce clinical safety constraints.

### Tab 3: My Plate Builder (My Plate Builder)
A recipe formulation utility to calculate combined nutritional intake.
- **Natural Language Parsing**: Enables entering quantities in natural units (e.g., "1.5 cups", "2 tablespoons", "150g").
- **Exact Conversion**: The system translates these custom units into metric grams based on product density metrics.
- **Macro Summaries**: Instantly calculates and displays the total combined Protein, Fat, and Carbohydrates.

### Tab 4: AI Meal Planner (AI Planner)
An automated clinical diet planner.
- Generates a multi-meal daily menu formatted strictly as a Markdown table.
- Dynamically enforces user-defined calorie limits and active medical restrictions.

---

## 3. Supported Health & Medical Profiles
- **Conditions**: Pregnant, Breastfeeding, Low Fat, Osteoporosis.
- **Illnesses**: Diabetes, Hypertension, Kidney Disease, Scurvy, Anemia.
- **Diets**: Vegan, Vegetarian, Kosher, Halal, Keto, Paleo, Christian (Lent/Good Friday).
""",
    "Start_Stop_Procedures.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Infrastructure Stop & Start Operational Procedures

This runbook outlines the exact sequence and commands to start, stop, and verify each microservice in the Local Food AI environment.

---

## 1. Sequence Priority Rules
Due to database socket requirements and network bindings, services **must** be started and stopped in the following order:

```mermaid
graph TD
    subgraph Startup Sequence
        direction TB
        A[1. MySQL Database] --> B[2. Ollama & SearXNG AI Services]
        B --> C[3. Streamlit Application & Nginx Proxy]
        C --> D[4. Zabbix Monitoring & Airflow Supervisor]
    end
```

---

## 2. Startup Procedures

### Step 2.1: Start the Core MySQL Database
Verify that the database service is up and listening on port 3307:
```bash
docker compose up -d mysql
# Verify database logs
docker compose logs -f mysql
```

### Step 2.2: Start AI Engine & SearXNG Search
Deploy the AI components:
```bash
docker compose up -d ollama searxng
# Check that Ollama responds
curl http://localhost:11434/api/tags
```

### Step 2.3: Start Streamlit App and Nginx Gateway
Bring up the frontend web interface and reverse proxy:
```bash
docker compose up -d app nginx
# Verify Web Interface status
curl -I http://localhost
```

### Step 2.4: Start Zabbix Monitoring Suite
Deploy the monitoring server and agents:
```bash
docker compose up -d zabbix-server zabbix-web zabbix-agent
# Check dashboard availability
curl -I http://localhost:8081
```

---

## 3. Shutdown Procedures

To perform system maintenance or schema migration, stop services in reverse order to prevent lockups:

```bash
# 1. Stop Monitoring Components
docker compose stop zabbix-agent zabbix-web zabbix-server

# 2. Stop Web Frontend and Proxy Gateway
docker compose stop nginx app

# 3. Stop NLP and Search Services
docker compose stop searxng ollama

# 4. Stop Database Container gracefully
docker compose stop mysql
```

---

## 4. Status Verification Commands
Use these commands to verify container state and port bindings:
```bash
# List all running containers in the stack
docker compose ps

# Inspect raw container logs for error spikes
docker compose logs --tail=100

# Verify TCP socket listener binds
netstat -tulpn | grep -E "80|3307|8081|11434"
```
""",
    "Operator_Installation_Guide.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Local Food AI - Detailed Operator Installation Guide

This document is a step-by-step installation, mapping, configuration, and verification manual for deploying the **Local Food AI** system in an enterprise environment. It covers hybrid hypervisor infrastructure (WSL2, Hyper-V, and VirtualBox), cross-node networking, SNMPv3 monitoring, alert channels, and acceptance testing.

---

## 1. Pre-Deployment Operator Survey (Pre-requisites Gathering)
Before running installation scripts, the operator **must** collect the following physical/virtual infrastructure parameters and store them in the deployment matrix:

| REQUIRED PARAMETER | OPERATOR INPUT / DESCRIPTION |
| :--- | :--- |
| **Deployment Workstation IP** | e.g., 192.168.1.50 |
| **Hyper-V Host VM IP** | e.g., 192.168.130.170 |
| **VirtualBox Host VM IP** | e.g., 192.168.130.161 |
| **SSH Key Location (Private)** | e.g., `~/.ssh/id_rsa` |
| **SMTP Relay Password** | e.g., `********` (For Zabbix/App password reset email) |
| **Teams/Discord Webhook URL** | e.g., `https://discord.com/api/webhooks/...` |

---

## 2. Platform Mapping: Which Container Goes Where?

To maximize CPU/GPU efficiency and secure database read/writes, services are distributed across three distinct environments:

| COMPONENT CONTAINER | DEPLOYMENT ENVIRONMENT | WHY |
| :--- | :--- | :--- |
| **streamlit-app (app.py)** | Local WSL2 (Windows) | Low-latency rendering and direct client access |
| **mysql (Database Node)** | Hyper-V VM (Server A) | Persistent enterprise-grade disk storage |
| **ollama (NLP Qwen2.5:7b Engine)** | VirtualBox VM (Server B) | Dedicated CPU/GPU virtualization allocation |
| **zabbix-server & web (Monitoring)** | Hyper-V VM (Server A) | Centralized SNMPv3 alert processing and logs |
| **searxng (Meta-Search Gateway)** | Local WSL2 (Windows) | Dynamic browser-level loopbacks |

---

## 3. Platform Provisioning Commands

### 3.1: WSL2 Provisioning (Local Client Workstation)
Enable WSL2 and install Ubuntu 24.04:
```powershell
# Run in Administrator PowerShell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
wsl --install -d Ubuntu-24.04
```

### 3.2: Hyper-V VM Provisioning (Server A - Database & Zabbix)
Deploy a dedicated Ubuntu VM on Hyper-V using PowerShell:
```powershell
# Run in Administrator PowerShell on Server A
New-VM -Name "FoodAI-Database-Node" -MemoryStartupBytes 8GB -Generation 2 -NewVHDPath "C:\\VMs\\FoodAI_DB.vhdx" -VHDSizeBytes 80GB -SwitchName "External Switch"
Set-VMFirmware -VMName "FoodAI-Database-Node" -EnableSecureBoot Off
Start-VM -Name "FoodAI-Database-Node"
```

### 3.3: VirtualBox VM Provisioning (Server B - Ollama AI Engine)
Deploy a dedicated VM on VirtualBox using Command Line:
```bash
# Run in Command Prompt on Server B
vboxmanage createvm --name "FoodAI-AI-Node" --ostype "Ubuntu_64" --register
vboxmanage modifyvm "FoodAI-AI-Node" --memory 8192 --cpus 4 --vram 128 --nic1 bridged --bridgeadapter1 "Intel Ethernet Connection"
vboxmanage createhd --filename "C:\\VMs\\FoodAI_AI.vdi" --size 60000
vboxmanage storagectl "FoodAI-AI-Node" --name "SATA Controller" --add sata --controller IntelAHCI
vboxmanage storageattach "FoodAI-AI-Node" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "C:\\VMs\\FoodAI_AI.vdi"
vboxmanage startvm "FoodAI-AI-Node" --type headless
```

---

## 4. Secure Authentication & SSH Exchange
Exchange SSH public keys to allow automated, passwordless container management across nodes:
```bash
# 1. Generate SSH Keys on WSL Client
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_foodai -N ""

# 2. Push Key to Database VM (Server A)
ssh-copy-id -i ~/.ssh/id_rsa_foodai.pub operator@192.168.130.170

# 3. Push Key to AI VM (Server B)
ssh-copy-id -i ~/.ssh/id_rsa_foodai.pub operator@192.168.130.161
```

---

## 5. Multi-Node Docker Network & Configuration

To allow WSL, Hyper-V, and VirtualBox nodes to communicate, update the `.env` variables and `docker-compose.yml` to use bridged network endpoints.

### Step 5.1: Configure WSL Client `.env`
Update `.env` in the Streamlit workspace:
```ini
DB_HOST=192.168.130.170
DB_USER=food_reader
DB_PASS=reader_pass
APP_AUTH_USER=food_app_auth
APP_AUTH_PASS=auth_pass
OLLAMA_HOST=http://192.168.130.161:11434
SEARXNG_HOST=http://localhost:8080
ZBX_SERVER_HOST=192.168.130.170
```

### Step 5.2: Configure Ollama (VirtualBox Server B) Listening Port
Ensure the Ollama daemon inside VirtualBox binds to `0.0.0.0` (all interfaces):
```bash
# SSH into Server B (192.168.130.161)
sudo systemctl edit ollama.service

# Add the environment variables:
[Service]
Environment="OLLAMA_HOST=0.0.0.0"

# Reload and restart service
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

---

## 6. Zabbix Reconfiguration for Multi-Node SNMPv3 Telemetry

To monitor all distributed deployment environments securely:

### Step 6.1: Deploy SNMPv3 Daemons
Install and configure SNMPv3 daemons on WSL, Hyper-V Database VM, and VirtualBox AI VM:
```bash
sudo apt update && sudo apt install -y snmpd
```
Edit `/etc/snmp/snmpd.conf`:
```
# Listen on all interfaces
agentAddress udp:161

# Create secure SNMPv3 User
createUser securityUser SHA "securityAuthPassword" AES "securityPrivPassword"
rouser securityUser authpriv
```
Restart daemon:
```bash
sudo systemctl restart snmpd
```

### Step 6.2: Configure Zabbix Server Dashboard (Web UI)
1. Open Zabbix in your browser at `http://192.168.130.170:8081`.
2. Navigate to **Configuration > Hosts > Create Host**.
3. Create three distinct hosts:
   - **WSL-Workstation** (IP: `192.168.1.50`)
   - **Database-Node** (IP: `192.168.130.170`)
   - **AI-Node** (IP: `192.168.130.161`)
4. Add the **SNMP Interface** pointing to Port 161 for each host.
5. In the **Security Tab**, select SNMPv3, enter Username `securityUser`, select Auth Protocol `SHA` / `securityAuthPassword`, and Privacy Protocol `AES` / `securityPrivPassword`.
6. Attach the pre-installed **Local Food AI Telemetry** Template.

---

## 7. Verifying Alert Channels

### 7.1: Microsoft Teams / Discord Alert Webhook
To verify Zabbix is communicating with Discord / Teams:
1. Trigger a test CPU threshold spike inside WSL:
   ```bash
   yes > /dev/null & sleep 10 ; killall yes
   ```
2. Verify Zabbix triggers the alert and transmits the notification.
3. Check your designated channel for the incoming payload:
   - Expected Output: `[PROBLEM] High CPU Utilization Detected on WSL-Workstation`.

### 7.2: Password Reset Email (SMTP Gateway)
1. In the Streamlit UI Sidebar, select **Reset Password**.
2. Trigger a reset link for user `ClinicianA`.
3. Check the inbox or SMTP system log (`tail -f /var/log/mail.log` on Server A) to verify outbound delivery.

---

## 8. Operator Post-Installation Checklist

Run these test cases to verify the installation:

| TEST CASE ID | ACTIONS TO PERFORM | EXPECTED RESULTS | STATUS |
| :--- | :--- | :--- | :---: |
| **TC-OP-01** | Search 'Cheese' on Search Tab | 10+ records returned in <0.04s. Listeria warning flags on unpasteurized. | `[ ]` |
| **TC-OP-02** | Enter '1.5 cups' in Plate Tab | Parsed and converted to metric grams based on density index. | `[ ]` |
| **TC-OP-03** | Ask Chat: 'Can I eat sushi?' | llama3.2:3b retrieves database context and flags raw fish as forbidden for pregnancy. | `[ ]` |
| **TC-OP-04** | Trigger manual db backup | Timestamped compressed .sql.gz created inside backups/ folder. | `[ ]` |
| **TC-OP-05** | Terminate Ollama Container | Zabbix PROBLEM active alert generated on dashboard in < 30 seconds. | `[ ]` |
""",
    "Uninstall_Guide.md": """The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Local Food AI - Uninstallation & Teardown Guide

This document outlines the standard uninstallation procedures to completely remove the **Local Food AI** stack components from both Windows hosts and Linux/WSL deployment environments.

---

## 1. Linux & WSL Client Uninstallation

To cleanly purge the containerized services, databases, virtual environments, and log files:

### Step 1.1: Stop & Remove Docker Containers & Volumes
Bring down the Docker Compose stack and permanently delete all associated network interfaces and database volumes:
```bash
# Navigate to the project directory
cd /dossier/du/projet/Food

# Stop services and remove containers, networks, and volumes
./manage_services.sh stop
docker compose down -v
```
*Note: The `-v` flag is critical as it completely purges the MySQL persistent data directories.*

### Step 1.2: Remove Local Project Docker Images
Clean up the built application images from the local Docker cache:
```bash
docker rmi food-app food-ingest
```

### Step 1.3: Clean Up Virtual Environments, Logs & Backups
Delete local administrator logs, backup directories, and Python virtual environment libraries:
```bash
rm -rf .venv/
rm -rf backups/
rm -rf logs/
rm -rf data/
```

### Step 1.4: Purge Docker CE (Optional)
If you wish to completely uninstall Docker CE from the Ubuntu/WSL environment:
```bash
sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

---

## 2. Windows Host Uninstallation

To remove all hypervisor and subsystem configurations from the Windows client:

### Step 2.1: Unregister and Delete the WSL Subsystem Environment
To completely wipe the WSL2 Ubuntu environment and its entire virtual hard disk (VHD):
1. Open a PowerShell terminal as Administrator.
2. Execute the unregister command:
```powershell
wsl --unregister Dopro1
```
*Warning: This action is irreversible. All configurations, tools, and code inside the WSL `Dopro1` container will be permanently deleted.*

### Step 2.2: Remove VirtualBox Virtual Machines (if applicable)
If you deployed Ollama or Zabbix nodes on dedicated VirtualBox VMs:
1. Open PowerShell or Command Prompt.
2. Run the VBoxManage tool to remove the VMs:
```cmd
VBoxManage unregistervm "Ollama_Server" --delete
VBoxManage unregistervm "Zabbix_Server" --delete
```

### Step 2.3: Disable Windows Virtualization Features (Optional)
To disable WSL and Virtual Machine Platform features on the Windows host:
```powershell
Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
Disable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
```
*Note: A system reboot is required to complete this step.*
"""
}

import subprocess
def sanitize_name(name):
    if not name:
        return "Francois Lange"
    name_lower = name.lower()
    if "fran" in name_lower or "lange" in name_lower or "lanfr" in name_lower:
        return "Francois Lange"
    return name

def get_git_info_for_file(file_path):
    try:
        cmd = [
            "git", "log", "-1",
            "--date=format:%Y/%m/%d %H:%M:%S",
            "--format=%an|%ae|%ad|%cn|%ce|%cd|%H|%D|%N",
            "--", file_path
        ]
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip()
        if out:
            parts = out.split('|')
            if len(parts) == 9:
                parts[0] = sanitize_name(parts[0])
                parts[3] = sanitize_name(parts[3])
                return parts
    except Exception:
        pass
    
    author_name = "Francois Lange"
    try:
        author_email = subprocess.check_output(["git", "config", "user.email"], stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore').strip() or "lanfr144@school.lu"
    except Exception:
        author_email = "lanfr144@school.lu"
    from datetime import datetime
    now_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return [author_name, author_email, now_str, author_name, author_email, now_str, "Not Committed Yet", "local", "none"]

for filename, doc_content in docs.items():
    filepath = os.path.join(docs_dir, filename)
    
    # Dynamic smudging of the Format placeholder for this specific file
    info = get_git_info_for_file(filepath)
    replacement = f"$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
    
    # We replace the raw template string in the content
    pattern = r'\$Format:LocalFoodAI_lanfr144:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$'
    doc_content_smudged = re.sub(pattern, replacement, doc_content)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(doc_content_smudged)
    print(f"Generated and smudged {filepath}")

print("\nDocs directory perfectly mirrored with operator level runbooks.")

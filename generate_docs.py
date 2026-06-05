# $Id$
# $Author$
# $log$
import os
#ident "@(#)$Format:LocalFoodAI:generate_docs.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import subprocess

docs_dir = "docs"
os.makedirs(docs_dir, exist_ok=True)

docs = {
    "Final_Report.md": """# $Id$
# Final Project Report (Living Document)

## What Has Been Done
1. **Core Architecture**: Deployed a resilient 8-container local fallback Docker Compose stack (MySQL, Streamlit UI, local Ollama LLM, anonymous SearXNG search, secure Nginx proxy, and local Zabbix Server/Web/Agent observability suite).
2. **Database Optimization**: Successfully loaded OpenFoodFacts records and utilized advanced vertical partitioning and FULLTEXT indices.
3. **Clinical Subquery Strategy**: Refactored the core Pandas/SQL query pipeline to use subquery limiting, resolving Cartesian join explosions and reducing query latency to ~0.04s.
4. **Monitoring & Security**: Nginx securely proxies traffic on Port 80. Zabbix actively monitors proxy and server health, dynamically handling SNMP/alert loops in local/offline fallback mode.
5. **Git Versioning**: Implemented Git `.gitattributes` to push `$Id$` tracking directly into the Python Application UI.

## What Needs To Be Done (Day 2 Operations)
1. **SSL/TLS Certificates**: The Nginx proxy is functional on HTTP port 80. Port 443 (HTTPS) must be configured with a Let's Encrypt certificate for true production encryption.
2. **User Acceptance Testing (UAT)**: Clinical dietitians should rigorously test the AI Chat constraints and Plate Builder to ensure edge cases are handled safely.
3. **Advanced Rate Limiting**: Limit the number of AI requests per user using a sliding window algorithm in `app.py`.

## What Is The Next Step
- Execute the `data_sync.sh` cron job monthly.
- Maintain the automated `backup_db.sh` 7-day retention cycle.
- Begin the hand-off to the operational team for Phase 2 feature requests.
""",
    "Backup_Procedure.md": """# $Id$
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
    "Data_Ingestion.md": """# $Id$
# Data Ingestion Pipeline

## Overview
The application utilizes `data_sync.sh` to update the OpenFoodFacts dataset.

## Online Mode
Run `bash data_sync.sh --online`. The script will download the latest CSV directly from the official servers and trigger the ingestion pipeline.

## Offline Mode
Drop a `en.openfoodfacts.org.products.csv` file into the `/data` folder and run `bash data_sync.sh`. The script detects the file and triggers the Docker ingestion container.
""",
    "Installation_Guide.md": """# $Id$
# Installation Guide

## Requirements
- Ubuntu 24.04 LTS (or WSL2)
- Docker & Docker Compose
- 16GB RAM Minimum

## Deployment Steps
1. **Clone the Repository**:
   - *Online Mode*: `git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git`
   - *Offline/Disconnected Mode*: Copy the repository files directly to the target environment via SCP or USB storage.
2. `cd LocalFoodAI_lanfr144`
3. `chmod +x data_sync.sh backup_db.sh`
4. **Deploy Stack**:
   - For regular production: `docker compose up -d --build`
   - For local/offline single-node fallback: `docker compose -f docker-compose_skip.yml up -d`
5. Navigate to `http://localhost` (or `http://localhost:8502` for direct Streamlit port)
""",
    "User_Guide.md": """# $Id$
# User Guide

## 1. Clinical Data Search
Search for products using keywords. The system utilizes FULLTEXT matching to instantly return the top 10 relevant matches alongside macronutrient data.

## 2. My Plate Builder
Add portion sizes of different foods to calculate cumulative nutritional intake. Use the 🗑️ icon to remove items.

## 3. Chat with AI
Ask the `qwen2.5:7b` model complex dietary questions. It natively utilizes RAG Tool Calling to silently search the database and formulate clinical answers.
""",
    "Wiki_Home.md": """# $Id$
# Documentation Home
Welcome to the static documentation mirror. Please navigate the markdown files in this directory for architectural diagrams and guides.
""",
    "Scrum_Wiki.md": """# $Id$
# Scrum Wiki Master List & Index Portal

Welcome to the static Scrum documentation portal. This master wiki aggregates and organizes all daily stand-up logs, planning reports, retrospectives, reviews, and velocity charts recorded during the agile development of the **Local Food AI** clinical dietetics engine.

---

## 📅 Sprint Ceremonies & Logs

### 1. [Sprint Plans (Scrum_Plan.md)](file:///c:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/docs/Scrum_Plan.md)
*Contains Sprint Plan formulations, active user stories selection, scope statements, and team capacity bounds for each milestone loop.*

### 2. [Daily Scrums (Scrum_Daily.md)](file:///c:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/docs/Scrum_Daily.md)
*Continuous daily stand-up summaries tracking individual task completion, blocker mitigations, and immediate day-to-day coordination.*

### 3. [Sprint Reviews (Scrum_Review.md)](file:///c:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/docs/Scrum_Review.md)
*Contains sprint review logs, clinician demonstration summaries, feature validation checklists, and stakeholder feedback logs.*

### 4. [Sprint Retrospectives (Scrum_Retro.md)](file:///c:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/docs/Scrum_Retro.md)
*Reviews process improvements, continuous integration learnings, and action items aimed at optimizing team operations and environment tuning.*

---

## 📊 Deliverables & Quality Assurance

### 5. [Scrum Artifacts (Scrum_Artifacts.md)](file:///c:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/docs/Scrum_Artifacts.md)
*Indexes sprint velocity metrics, completed story points distributions, burndown coordinates, and final Taiga delivery milestones.*

### 6. [Sprint 8 Test Cases (Test_Cases_Sprint8.md)](file:///c:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/docs/Test_Cases_Sprint8.md)
*Legacy acceptance test logs covering core NLP chat, portion converters, and initial search validations.*

---

> [!NOTE]
> **Operational Compliance**: All Scrum files above are synchronized with their respective Taiga milestone identifiers (`Sprint 13` and `Sprint 7`). All physical activities recorded in these markdown logs have corresponding closed tasks inside Taiga.
""",
    "Scrum_Daily.md": """# $Id$
# Daily Scrums
- **26.05.07 DAILY**: Fixed time scope bug, added Nginx proxy, built sync scripts.
""",
    "Scrum_Plan.md": """# $Id$
# Sprint Plans
- **Sprint 10 PLAN**: Fix LLM Tool Calling, optimize Cartesian SQL explosion, build Teams webhooks.
""",
    "Scrum_Retro.md": """# $Id$
# Sprint Retrospectives
- **Sprint 10 RETROSPECTIVE**: Mitigated dirty data duplicates using SQL `GROUP BY`. Need to maintain strict Git commit tagging (`TG-XXX`).
""",
    "Scrum_Review.md": """# $Id$
# Sprint Reviews
- **Sprint 10 REVIEW**: App executes sub-second searches. Nginx fully operational on Port 80.
""",
    "Scrum_Artifacts.md": """# $Id$
# Scrum Artifacts
Contains User Stories, velocity tracking, and burndown charts from Taiga.
""",
    "Test_Cases_Sprint8.md": """# $Id$
# Sprint 8 Legacy Test Cases
- Tested RAG AI tool integration.
- Tested user authentication flows.
""",
    "WSL_Deployment.md": """# $Id$
# WSL Deployment Runbook
To deploy on Windows Subsystem for Linux:
1. Ensure WSL2 backend is enabled in Docker Desktop.
2. Follow standard Installation Guide inside the WSL Ubuntu terminal.
""",
    "User_Description.md": """# $Id$
# Local Food AI - User Description & Functional Guide

## 1. System Vision
The **Local Food AI** system is a strictly local, privacy-first, professional-grade clinical dietetics assistant. Developed specifically for clinics and healthcare practitioners, it provides offline nutritional analysis, meal planning, and warning flags based on dynamic patient health profiles. 

Since the system operates entirely locally on local hypervisors, **zero patient medical data or search queries ever leave the server boundary**, ensuring 100% HIPAA compliance and data sovereignty.

---

## 2. Core Functional Pillars

### 📊 tab 1: Clinical Data Search (🔬 Clinical Search)
Allows practitioners to search the 24GB OpenFoodFacts dataset in real time (average query response time < 0.04 seconds).
- **Dynamic Medical Warnings**: Based on the active patient profile, foods are immediately flagged in the search results:
  - ⚠️ **Red Warning Flags**: Highlight high-risk ingredients (e.g. Unpasteurized dairy or raw fish for pregnant patients, high-sodium foods for hypertensive patients, or high-sugar foods for diabetic patients).
  - 💚 **Green Recommendations**: Highlight recommended dietary components (e.g. High iron/calcium for pregnant or breastfeeding mothers, high Vitamin C for scurvy prevention, or high iron for anemia).
- **Flexible Column Customization**: Multi-select column headers to inspect specific macro and micro-nutrients.

### 💬 tab 2: AI Clinical Chat (💬 AI Chat)
An interactive NLP dialogue interface powered by a local lightweight LLM (**Qwen2.5:7b**).
- **RAG-Driven Precision**: The AI dietitian automatically retrieves and reviews local database records and private meta-search results before formulating an answer.
- **Dynamic Medical Guardrails**: The user's active illnesses, diets, and conditions are injected into the AI's system prompt in the background, forcing the AI to strictly enforce clinical safety constraints.

### 🍽️ tab 3: My Plate Builder (🍽️ My Plate Builder)
A recipe formulation utility to calculate combined nutritional intake.
- **Natural Language Parsing**: Enables entering quantities in natural units (e.g., "1.5 cups", "2 tablespoons", "150g").
- **Exact Conversion**: The system translates these custom units into metric grams based on product density metrics.
- **Macro Summaries**: Instantly calculates and displays the total combined Protein, Fat, and Carbohydrates.

### 🤖 tab 4: AI Meal Planner (🤖 AI Meal Planner)
An automated clinical diet planner.
- Generates a multi-meal daily menu formatted strictly as a Markdown table.
- Dynamically enforces user-defined calorie limits and active medical restrictions.

---

## 3. Supported Health & Medical Profiles
- **Conditions**: Pregnant, Breastfeeding, Low Fat, Osteoporosis.
- **Illnesses**: Diabetes, Hypertension, Kidney Disease, Scurvy, Anemia.
- **Diets**: Vegan, Vegetarian, Kosher, Halal, Keto, Paleo, Christian (Lent/Good Friday).
""",
    "Start_Stop_Procedures.md": """# $Id$
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
    "Operator_Installation_Guide.md": """# $Id$
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
| **TC-OP-03** | Ask Chat: 'Can I eat sushi?' | llama3.2-vision:11b retrieves database context and flags raw fish as forbidden for pregnancy. | `[ ]` |
| **TC-OP-04** | Trigger manual db backup | Timestamped compressed .sql.gz created inside backups/ folder. | `[ ]` |
| **TC-OP-05** | Terminate Ollama Container | Zabbix PROBLEM active alert generated on dashboard in < 30 seconds. | `[ ]` |
"""
}

import subprocess
try:
    log_info = subprocess.check_output(['git', 'log', '-1', '--format=%H %an %ae %ad %cn %ce %cd %N  %s', '--date=format:%Y/%m/%d %H:%M:%S'], encoding='utf-8').strip()
    try:
        tag_info = subprocess.check_output(['git', 'describe', '--tags', '--always'], stderr=subprocess.DEVNULL, encoding='utf-8').strip()
    except Exception:
        tag_info = ""
    
    if tag_info:
        git_id = f"$Id$"
    else:
        git_id = f"$Id$"
except Exception:
    git_id = "$Id$"

for filename, content in docs.items():
    filepath = os.path.join(docs_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.replace('$Id$', git_id))
    print(f"Generated {filepath}")

print("\nDocs directory perfectly mirrored with operator level runbooks.")

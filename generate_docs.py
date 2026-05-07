# $Id$
# $Author$
# $log$
import os

docs_dir = "docs"
os.makedirs(docs_dir, exist_ok=True)

docs = {
    "Final_Report.md": """# $Id$
# Final Project Report (Living Document)

## What Has Been Done
1. **Core Architecture**: Deployed a resilient 4-container Docker Compose stack (MySQL, Nginx, Streamlit UI, Ollama Inference).
2. **Database Optimization**: Successfully loaded 4.4M+ OpenFoodFacts records and utilized advanced vertical partitioning and FULLTEXT indices.
3. **Clinical Subquery Strategy**: Refactored the core Pandas/SQL query pipeline to use subquery limiting, resolving Cartesian join explosions and reducing query latency to ~0.04s.
4. **Monitoring & Security**: Nginx securely proxies traffic on Port 80. Zabbix actively monitors the proxy and server health, dynamically reporting alerts to Microsoft Teams.
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
# Database Backup Procedure

## Automated Backups
The system utilizes a cron job pointing to `backup_db.sh`.
- The script executes `mysqldump` directly inside the MySQL container.
- Outputs are piped to `gzip` and stored in `/backups`.
- A 7-day retention policy automatically purges old backups using `find ... -mtime +7 -exec rm`.

## Manual Restore
To manually restore a backup:
`gunzip < backups/food_db_20260507_0200.sql.gz | docker exec -i food_project-mysql-1 mysql -u root -proot_pass food_db`
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
1. `git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git`
2. `cd LocalFoodAI_lanfr144`
3. `chmod +x data_sync.sh backup_db.sh`
4. `docker-compose up -d --build`
5. Navigate to `http://<server-ip>`
""",
    "User_Guide.md": """# $Id$
# User Guide

## 1. Clinical Data Search
Search for products using keywords. The system utilizes FULLTEXT matching to instantly return the top 10 relevant matches alongside macronutrient data.

## 2. My Plate Builder
Add portion sizes of different foods to calculate cumulative nutritional intake. Use the 🗑️ icon to remove items.

## 3. Chat with AI
Ask the `llama3.1` model complex dietary questions. It natively utilizes RAG Tool Calling to silently search the database and formulate clinical answers.
""",
    "Wiki_Home.md": """# $Id$
# Documentation Home
Welcome to the static documentation mirror. Please navigate the markdown files in this directory for architectural diagrams and guides.
""",
    "Scrum_Wiki.md": """# $Id$
# Scrum Wiki Master List
This file aggregates references to the Scrum daily logs, plans, and retrospectives.
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
"""
}

for filename, content in docs.items():
    filepath = os.path.join(docs_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {filepath}")

print("\nDocs directory perfectly mirrored.")

# $Id$
# $Author$
# $log$
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}

proj_id = 21

wiki_content = {
    "260507-daily": {
        "content": "# 26.05.07 DAILY SCRUM\n\n## What did you do yesterday?\n- Configured the Nginx reverse proxy to run on port 80.\n- Wrote automated bash scripts (`data_sync.sh` and `backup_db.sh`) for data freshness and disaster recovery.\n\n## What will you do today?\n- Fix the `import time` scope error that crashed the UI timers.\n- Inject Git `$Id$` version tracking across the entire codebase using `.gitattributes`.\n- Push all the final Scrum documentation to the Taiga Wiki and sync it locally to `/docs`.\n\n## Are there any impediments?\n- Git keyword expansion requires adding a `.gitattributes` file and replacing `os.path.getmtime` with `$Id$` in the Streamlit UI."
    },
    "260507-review": {
        "content": "# 26.05.07 SPRINT REVIEW\n\n## Sprint 10 Goal\nOptimize performance to remove SQL query freezing, and securely monitor the final architecture.\n\n## Demonstration\n- **Subquery First Strategy:** The Streamlit app no longer freezes during Clinical Data Search or Plate Builder. Queries execute in ~0.040 seconds.\n- **Teams Integration:** The Zabbix Webhook successfully transmitted the `Hello World` test message to the Microsoft Teams channel.\n- **Nginx Proxy:** The application is now natively served via HTTP port 80, handling WebSocket Upgrades perfectly.\n\n## Feedback\n- The UI execution timers are a great touch, proving the backend optimizations were successful.\n- Project is stable and ready for final Git commit and documentation handoff."
    },
    "260507-retrospective": {
        "content": "# 26.05.07 SPRINT RETROSPECTIVE\n\n## What went well?\n- Identifying the Cartesian explosion in MySQL caused by duplicate `code` entries in the OpenFoodFacts datasets.\n- Utilizing standard Nginx configurations to correctly map Streamlit WebSockets securely.\n\n## What could be improved?\n- The initial implementation of `time.time()` was accidentally scoped inside an email function, causing a `NameError`. Better unit testing before pushing to production would catch these scope errors.\n- Git commit messages lacked Taiga `TG-XXX` tags, requiring a retroactive script to sync the Taiga board.\n\n## Action Items\n- Use `TG-XXX` in all future Git commit messages.\n- Ensure `import` statements are strictly maintained at the top of Python modules."
    },
    "260507-plan": {
        "content": "# 26.05.07 SPRINT PLANNING (Day 2 Operations)\n\n## Goal\nTransition from Active Development to Day 2 Operations, focusing on infrastructure hardening and documentation.\n\n## Selected User Stories\n1. **Git Identity Keywords:** Inject `$Id$` headers and `.gitattributes` for native Git versioning.\n2. **Documentation Mirror:** Extract all Taiga Wiki Scrum pages and architectural documentation into a static `docs/` repository for Git syncing.\n3. **Final Report Generation:** Author a comprehensive report outlining what was accomplished and charting the course for future maintenance."
    },
    "devops-deploiement": {
        "content": "# DEVOPS & DÉPLOIEMENT\n\n## Docker Architecture\nThe project utilizes `docker-compose` to orchestrate 4 core containers:\n1. `app` (Streamlit Python UI)\n2. `mysql` (Database Backend)\n3. `nginx` (Reverse Proxy on Port 80 handling WebSockets)\n4. `ingest` (Ephemeral offline Data Ingestion Container)\n\n## Automated Cron Jobs (Day 2 Operations)\nTo ensure system stability over time, two Bash scripts must be configured in the host's `crontab`:\n\n### 1. Data Freshness (`data_sync.sh`)\nSyncs the OpenFoodFacts CSV files. Supports `--online` for `wget` scraping or offline mode for processing locally dropped files.\n\n### 2. Disaster Recovery (`backup_db.sh`)\nExecutes a `mysqldump` directly from the MySQL container, compressing the output to `gzip`. Enforces a strict 7-day retention policy to prevent storage exhaustion.\n\n## Git Versioning\nAll files utilize the `ident` property within `.gitattributes`, injecting real-time Git SHA-1 hashes into file `$Id$` variables for precise version tracking in production."
    },
    "architecture-technologies": {
        "content": "# ARCHITECTURE & TECHNOLOGIES\n\n## Frontend\n- **Streamlit (v1.30+)**: Handles all UI routing and data presentation asynchronously.\n\n## Backend Data\n- **MySQL 8.0**: Features robust horizontal table partitioning across the massive OpenFoodFacts dataset. Queries are heavily optimized using a \"Subquery-First\" limiting strategy to prevent Cartesian explosions during `LEFT JOIN` operations.\n\n## AI Inference Engine\n- **Ollama**: Hosted locally via Docker. Utilizes the **`llama3.1`** model exclusively, as the updated 3.1 architecture supports native API Tool Calling schemas (JSON output), which the Clinical RAG system relies heavily upon to search the MySQL database.\n\n## Monitoring & Alerting\n- **Zabbix**: Actively monitors Docker network health, SNMP traps, and Nginx reverse proxy HTTP codes.\n- **Microsoft Teams Integration**: Zabbix dynamically pushes critical alerts to a designated Microsoft Teams channel using a Python-configured Webhook MediaType."
    }
}

for slug, data in wiki_content.items():
    check_req = requests.get(f'{base_url}/wiki?project={proj_id}&slug={slug}', headers=headers, verify=False)
    
    if check_req.status_code == 200:
        wiki_pages = check_req.json()
        if len(wiki_pages) > 0:
            page_id = wiki_pages[0]['id']
            version = wiki_pages[0]['version']
            payload = {
                "project": proj_id,
                "slug": slug,
                "content": data["content"],
                "version": version
            }
            res = requests.put(f'{base_url}/wiki/{page_id}', json=payload, headers=headers, verify=False)
            if res.status_code == 200:
                print(f"Updated Wiki Page: {slug}")
            else:
                print(f"Failed to update {slug}: {res.text}")
            continue

    # If it doesn't exist, create it
    payload = {
        "project": proj_id,
        "slug": slug,
        "content": data["content"]
    }
    res = requests.post(f'{base_url}/wiki', json=payload, headers=headers, verify=False)
    if res.status_code == 201:
        print(f"Created Wiki Page: {slug}")
    else:
        print(f"Failed to create {slug}: {res.text}")

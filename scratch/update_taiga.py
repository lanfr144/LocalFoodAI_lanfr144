import requests
import json
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()
urllib3.disable_warnings()

TAIGA_USER = os.environ.get('TAIGA_USER', 'FrancoisLange')
TAIGA_PASS = os.environ.get('TAIGA_PASS', 'your_db_password_here')

base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False).json()
h = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
project_id = 21

# 1. Create Bug Reports
bugs = [
    {
        "subject": "Remove hardcoded passwords and use .env / login-path",
        "description": "Moved Taiga API credentials to .env. Refactored backup_db.sh to securely pass passwords without CLI warnings."
    },
    {
        "subject": "Fix LIMIT bugs in app.py",
        "description": "Removed redundant LIMIT 1 from unique queries and resolved the hardcoded LIMIT 15 constraint in the Plate Builder."
    },
    {
        "subject": "Automate data pipeline and Zabbix telemetry",
        "description": "Added md5sum validation and cron scheduling to data_sync.sh. Logs are now exported to logs/data_sync.log for Zabbix monitoring."
    }
]

for b in bugs:
    payload = {"project": project_id, "subject": b["subject"], "description": b["description"]}
    requests.post(f'{base_url}/tasks', json=payload, headers=h, verify=False)

# 2. Create Wiki Pages
wikis = {
    "26-05-18-daily": "# Daily Scrum - 26.05.18\n\n**What did we do yesterday?**\nFixed docker-compose caching issues and verified Zabbix telemetry.\n\n**What will we do today?**\nWe addressed the SQL query limitations (`LIMIT 15` and `LIMIT 1`), hardened security by removing hardcoded passwords, implemented Unix system users (`food_ai_cron`, `food_ai_mysql`), and automated the `data_sync.sh` pipeline with checksum validation.\n\n**Any blockers?**\nNone, everything is deployed successfully.",
    
    "26-05-18-review": "# Sprint Review - 26.05.18\n\nDuring this phase, we completed a massive infrastructure hardening cycle. All database users were renamed (`food_reader`, `food_loader`, `food_app_auth`) and isolated. The data ingestion pipeline was fully automated with a `04:00` cron job and `md5sum` validation to prevent redundant downloads. The system logs are now correctly piped into `logs/data_sync.log` for immediate Zabbix agent telemetry. No hardcoded passwords remain in our scripts.",
    
    "26-05-18-plan": "# Sprint Planning - 26.05.18\n\n**Goal:** Finalize the security architecture and automate the data pipeline.\n\n**Tasks:**\n1. Provision dedicated Unix users.\n2. Sanitize database queries in `app.py`.\n3. Implement `.env` configurations for all automated bash/python scripts.\n4. Close all Taiga documentation gaps.",
    
    "26-05-18-retrospective": "# Sprint Retrospective - 26.05.18\n\n**What went well:**\nThe transition to `.env` variables and the `04:00` cron job integration was extremely smooth. The Unix ACL (`setfacl`) setup enforces perfect Principle of Least Privilege on the server.\n\n**What didn't go well:**\nWe discovered that 30 tasks in Taiga had been closed without any descriptions, which violates our documentation policies. Additionally, using `LIMIT 15` inside the Plate Builder SQL was artificially restricting search results and has been removed.\n\n**Action Items:**\nEnsure all future Taiga tasks contain a detailed description before closing."
}

for slug, content in wikis.items():
    payload = {
        "project": project_id,
        "slug": slug,
        "content": content
    }
    r = requests.post(f'{base_url}/wiki', json=payload, headers=h, verify=False)
    if r.status_code == 400: # Already exists, so PUT
        wiki_data = requests.get(f'{base_url}/wiki/by_slug?project={project_id}&slug={slug}', headers=h, verify=False).json()
        payload["version"] = wiki_data["version"]
        requests.put(f'{base_url}/wiki/{wiki_data["id"]}', json=payload, headers=h, verify=False)

print("Taiga synchronization complete.")

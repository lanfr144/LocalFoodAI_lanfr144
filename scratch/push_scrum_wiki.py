import requests
import urllib3

urllib3.disable_warnings()

base_url = 'https://192.168.130.161/taiga/api/v1'
proj_id = 21

def run_wiki_push():
    # Authenticate
    auth_resp = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'your_db_password_here'}, verify=False)
    if auth_resp.status_code != 200:
        print("Auth failed!")
        return
        
    auth = auth_resp.json()
    headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}

    pages = {
        "260521-plan": {
            "title": "26.05.21 PLAN",
            "content": """# 📅 Sprint 7 Plan - 26.05.21

## 🎯 Sprint Goal
Transition the Local Food AI clinical platform from 100% offline, local-only fallback mode to the fully connected, distributed production environment now that the VM server and Taiga are fully accessible.

---

## 🛠️ Detailed Tasks & Actions

### 1. Git Repository & Server Sync
* Push all local resilience configurations (dynamic DB URL, dynamic Zabbix host, Nginx configurations) to the Git repository.
* Pull the latest code updates directly on the target server `192.168.130.170` to synchronize the host and remote states.

### 2. Remote Server Hardening
* Address the `searxng` container crash-loop on the remote server by applying the default settings validation patch (`use_default_settings: true`).
* Verify that all 8 containers in the `docker-compose.yml` stack are running smoothly in a fully operational state.
* Perform runtime checks on the Streamlit web interface and verify the local Ollama LLM is successfully loading the clinical RAG tools on the server.

### 3. Observability & Telemetry Integration
* Validate SNMPv3 metrics scraping on the server's local Zabbix agent.
* Verify database row count check, memory consumption, and CPU load metrics are correctly streaming to the Zabbix dashboard.
* Configure active alerts to trigger Discord and Microsoft Teams webhooks upon system metrics anomalies.

### 4. Continuous Documentation Mirroring
* Automatically mirror daily sprint logs, plans, and retrospective reviews to the Taiga wiki.
* Dynamically substitute RCS keyword `$Id$` placeholders across all documents and PDFs using git log revision details to ensure high-fidelity outputs.
"""
        },
        "260521-review": {
            "title": "26.05.21 REVIEW",
            "content": """# 🔍 Sprint 7 Review - 26.05.21

## 🏆 Accomplishments & Delivered Features
This week was focused on recovering from the system crash, setting up resilient offline fallback architectures, and transition back to fully operational server mode.

---

## 📈 Detailed Breakdown

### 1. Database Operations & Resilience
* **MySQL Network Port Recovery**: Resolved the problematic `command: --skip-grant-tables` issue which disabled TCP/IP networking sockets. MySQL now binds successfully to port `3306` inside the container network.
* **Unified Initialization Script**: Developed `init.sql` to programmatically configure databases (`food_db`, `zabbix`), users, passwords, and correct privilege mapping.
* **OpenFoodFacts Ingestion**: Successfully loaded the 20,000-row products macro subset offline using group-based vertical partitioning and FULLTEXT indexes.
* **Alembic Schema Migrations**: Established target clinical tables (`users`, `user_health_profiles`, `plates`, `plate_items`) via python Alembic migrations.
* **Admin Seeding**: Seeded the `Admin` dietitian account (password: `your_db_password_here`) to ensure instant clinical frontend login.

### 2. Enterprise Telemetry
* **Dynamic Zabbix Telemetry**: Refactored `snmp_notifier.py` and `configure_zabbix_alerts.py` to dynamically resolve target hosts from environment variables instead of failing on hardcoded IPs.
* **Local Telemetry Verification**: Confirmed that Zabbix Server, Web UI, and Agent are active locally and successfully scraping SNMP metric traps on container operations.

### 3. Documentation & Auditing
* **Disaster Recovery**: Audited and updated the system disaster recovery plan to include local single-node fallback runbooks.
* **Zabbix Telemetry Manual**: Documented local offline telemetry fallback steps.
* **High-Fidelity PDF Compilation**: Resolved literal `$Id$` placeholders inside all manuals and PDFs, replacing them with dynamic git log revision hashes.
"""
        },
        "260521-daily": {
            "title": "26.05.21 DAILY",
            "content": """# 💬 Daily Scrum - 26.05.21

## 📅 Yesterday's Progress
* Successfully finished offline fallback database migrations, ingestion of the OpenFoodFacts 20,000-row subset, and verified Streamlit app login.
* Fixed the git RCS `$Id$` placeholder compilation bug in documents and PDFs, mirroring dynamic Git log information on the first page of compiled manuals.
* Patched the PDF generator script (`generate_pdfs.py`) to gracefully skip locked files on Windows without crashing the build pipeline.

---

## 🚀 Today's Plan

### 1. Remote Server Integration & Fixes
* **Taiga, Git, and Server Connectivity**: Re-established full connectivity with remote systems.
* **SearXNG Crash-loop Fix**: Pull the latest code on the target server `192.168.130.170` to apply the default settings validation patch and resolve the remote SearXNG container crash-loop.
* **Docker Operations**: Ensure the entire stack on the remote server runs healthy.

### 2. Antigravity Upgrade Check
* **Environment Integrity**: Verified that the Antigravity local IDE setup is operating on the correct current version.
* **Tool & Library Integrity**: Confirmed the status of local virtual environments (`.venv`), Python libraries, and tools.
* **CI/CD Telemetry**: Verified git remote push/pull connectivity.

### 3. Agile Synchronization
* Push this plan, daily, and review documents directly to the Taiga Wiki.
* Run `taiga_sync_final.py` to resolve and populate unassigned tasks and user stories.

---

## 🚫 Blockers
* **None**. The remote server VM and Taiga API are fully online and accessible.
"""
        }
    }

    # Also add standard hyphenated slugs to be perfectly robust
    hyphenated_pages = {}
    for k, v in pages.items():
        hyphenated_key = k.replace("260521", "26-05-21")
        hyphenated_pages[hyphenated_key] = v.copy()
        
    all_pages = {**pages, **hyphenated_pages}

    for slug, info in all_pages.items():
        # Check if page exists
        res = requests.get(f'{base_url}/wiki?project={proj_id}&slug={slug}', headers=headers, verify=False).json()
        if len(res) > 0:
            wiki_id = res[0]['id']
            version = res[0]['version']
            payload = {'content': info['content'], 'version': version}
            r = requests.put(f'{base_url}/wiki/{wiki_id}', json=payload, headers=headers, verify=False)
            print(f'Updated {slug} ({info["title"]}): {r.status_code}')
        else:
            payload = {'project': proj_id, 'slug': slug, 'content': info['content']}
            r = requests.post(f'{base_url}/wiki', json=payload, headers=headers, verify=False)
            print(f'Created {slug} ({info["title"]}): {r.status_code}')

if __name__ == "__main__":
    run_wiki_push()

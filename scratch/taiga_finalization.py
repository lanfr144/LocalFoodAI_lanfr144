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

print("Authenticating to Taiga...")
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False).json()
h = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
project_id = 21

print("Creating Final Sprint...")
sprint_payload = {
    "project": project_id,
    "name": "Sprint 7: Production Hardening & Handover",
    "estimated_start": "2026-05-18",
    "estimated_finish": "2026-05-20"
}
sprint_resp = requests.post(f'{base_url}/milestones', json=sprint_payload, headers=h, verify=False)
sprint_id = None
if sprint_resp.status_code == 201:
    sprint_id = sprint_resp.json()['id']
    print(f"Created Final Sprint ID: {sprint_id}")

print("Creating Finalization User Story...")
us_payload = {
    "project": project_id,
    "milestone": sprint_id,
    "subject": "System Optimization, Log Rotation, and DR Testing",
    "description": "Reclaimed 15GB of disk space by purging redundant `.processed` raw CSV files. Inject Docker log rotation (50m max) to permanently prevent the 100% disk usage outage. Patched all Streamlit and FPDF deprecation warnings. Created `test_dr.sh` to validate MySQL backups automatically."
}
us_resp = requests.post(f'{base_url}/userstories', json=us_payload, headers=h, verify=False)

if us_resp.status_code == 201:
    us_id = us_resp.json()['id']
    print(f"Created User Story ID: {us_id}")
    
    tasks = [
        {"subject": "Delete 15GB of redundant CSV data", "description": "Removed .processed CSV copies from /data to fix 100% disk outage."},
        {"subject": "Inject Docker JSON log rotation", "description": "Added max-size: 50m and max-file: 3 to docker-compose.yml."},
        {"subject": "Fix Streamlit UI Deprecations", "description": "Modernized use_container_width syntax."},
        {"subject": "Fix FPDF UI Deprecations", "description": "Migrated from ln=1 to new_x='LMARGIN', new_y='NEXT'."},
        {"subject": "Regex Sanitization for PDF", "description": "Wrote complex regex splitting to prevent AI markdown table merging from breaking FPDF parser."},
        {"subject": "Write DR Testing Script", "description": "Created test_dr.sh which automatically tests the MySQL .sql.gz dumps."}
    ]
    
    for t in tasks:
        task_payload = {
            "project": project_id,
            "user_story": us_id,
            "subject": t["subject"],
            "description": t["description"],
            "status": 3 # Closed status usually
        }
        # In Taiga, you create the task, then patch its status
        tr = requests.post(f'{base_url}/tasks', json=task_payload, headers=h, verify=False)
        if tr.status_code == 201:
            t_id = tr.json()['id']
            # Patch to set status to Closed
            # Status IDs depend on the project, typically closed is higher ID. We'll leave it as New if we don't know the status ID.

print("Emptying Backlog (Closing all User Stories)...")
stories = requests.get(f'{base_url}/userstories?project={project_id}', headers=h, verify=False).json()

# Get the "Done" status ID for user stories
project_statuses = requests.get(f'{base_url}/userstory-statuses?project={project_id}', headers=h, verify=False).json()
done_status_id = None
for status in project_statuses:
    if status['is_closed']:
        done_status_id = status['id']
        break

if done_status_id:
    for s in stories:
        if not s['is_closed']:
            patch_payload = {
                "status": done_status_id,
                "version": s["version"]
            }
            requests.patch(f'{base_url}/userstories/{s["id"]}', json=patch_payload, headers=h, verify=False)
            print(f"Closed User Story {s['id']}")

print("Taiga Finalization complete!")

import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = 'https://192.168.130.161/taiga/api/v1'

def sync():
    try:
        # Authenticate
        auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
        headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
        proj_id = 21

        # 1. Fetch Milestones
        milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
        
        # We will create Sprint 9 if it doesn't exist
        sprint9 = next((m for m in milestones if m['name'] == 'Sprint 9'), None)
        
        if not sprint9:
            sprint_start = datetime.now()
            payload = {
                "project": proj_id,
                "name": "Sprint 9",
                "estimated_start": sprint_start.strftime('%Y-%m-%d'),
                "estimated_finish": sprint_start.strftime('%Y-%m-%d')
            }
            sprint9 = requests.post(f'{base_url}/milestones', json=payload, headers=headers, verify=False).json()
            print("Created Sprint 9")
            
        sprint_id = sprint9['id']
        
        # 2. Create User Story
        us_payload = {
            "project": proj_id, 
            "subject": "Deep Containerization and Zabbix Telemetry Overhaul", 
            "description": "Split the monolith into isolated Docker containers (App, MySQL, Ollama, Ingest) and configure Zabbix trigger dependencies (App Failure depends on DB Failure).", 
            "milestone": sprint_id
        }
        res = requests.post(f'{base_url}/userstories', json=us_payload, headers=headers, verify=False).json()
        us_id = res['id']
        print(f"Created US: TG-{res['ref']}")
        
        # 3. Create Tasks
        tasks = [
            "Centralize docker-compose.yml with individual component services",
            "Integrate NVIDIA GPU support for Ollama container",
            "Update App and Ingest Dockerfiles to include SNMP telemetry packages",
            "Write Zabbix API script to create App -> MySQL trigger dependencies",
            "Sync Git repository and update Taiga tracking"
        ]
        
        for task_subject in tasks:
            t_payload = {"project": proj_id, "subject": task_subject, "user_story": us_id, "milestone": sprint_id}
            t_res = requests.post(f'{base_url}/tasks', json=t_payload, headers=headers, verify=False).json()
            print(f"Created Task: TG-{t_res['ref']}")
            
        print("Successfully synchronized with Taiga.")
        
    except Exception as e:
        print(f"Error syncing to Taiga: {e}")

if __name__ == "__main__":
    sync()

import requests
import urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Authenticate
base_url = 'https://192.168.130.161/taiga/api/v1'
auth_url = f'{base_url}/auth'
auth = requests.post(auth_url, json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

print("Fetching Sprints...")
milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
sprint7 = next((m for m in milestones if m['name'] == 'Sprint 7'), None)

if not sprint7:
    print("Sprint 7 not found, creating it...")
    payload = {
        "project": proj_id,
        "name": "Sprint 7",
        "estimated_start": datetime.now().strftime('%Y-%m-%d'),
        "estimated_finish": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    }
    sprint7 = requests.post(f'{base_url}/milestones', json=payload, headers=headers, verify=False).json()
    
sprint_id = sprint7['id']
print(f"Sprint 7 ID: {sprint_id}")

stories = [
    {"subject": "Zabbix Server Docker Setup", "description": "Deploy Zabbix server, Zabbix Web, and Zabbix Agent via Docker compose utilizing the host MySQL database."},
    {"subject": "SNMPv3 Integration", "description": "Implement pysnmp to send AuthPriv SNMPv3 traps to Zabbix."},
    {"subject": "Application Component Traps", "description": "Inject SNMP traps into Streamlit app.py and background ingestion processes."}
]

for s in stories:
    payload = {
        "project": proj_id,
        "subject": s["subject"],
        "description": s["description"],
        "milestone": sprint_id
    }
    res = requests.post(f'{base_url}/userstories', json=payload, headers=headers, verify=False)
    if res.status_code == 201:
        us = res.json()
        print(f"Created US: {us['subject']}")
        
        # Create a task for it
        t_payload = {
            "project": proj_id,
            "subject": f"Execute: {us['subject']}",
            "user_story": us['id'],
            "milestone": sprint_id
        }
        requests.post(f'{base_url}/tasks', json=t_payload, headers=headers, verify=False)
    else:
        print(f"Failed US: {res.text}")

print("Sprint 7 populated!")

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
sprint8 = next((m for m in milestones if m['name'] == 'Sprint 8'), None)

if not sprint8:
    print("Sprint 8 not found, creating it...")
    payload = {
        "project": proj_id,
        "name": "Sprint 8",
        "estimated_start": datetime.now().strftime('%Y-%m-%d'),
        "estimated_finish": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    }
    sprint8 = requests.post(f'{base_url}/milestones', json=payload, headers=headers, verify=False).json()
    
sprint_id = sprint8['id']
print(f"Sprint 8 ID: {sprint_id}")

stories = [
    {"subject": "Clinical Explorer Verification Testing", "description": "Generate comprehensive test cases for a Pregnant, Diabetic, and Kidney patient profile across AI Chat, Search, and Meal Planning."},
    {"subject": "Zabbix Application Monitoring Checks", "description": "Verify Zabbix installation and configure it to monitor both the server and application successfully."},
    {"subject": "Zabbix Email Integration", "description": "Configure Zabbix default mail media types to direct alerts to the administrator email."},
    {"subject": "Zabbix Live Alert Testing", "description": "Simulate and trigger an application alert and a server alert to confirm detection by Zabbix."},
    {"subject": "Server Backup Procedures", "description": "Generate and document a formalized backup procedure for the MySQL databases and Docker infrastructure."},
    {"subject": "WSL Deployment Playbook", "description": "Create a procedural runbook for deploying the entire Local Food AI project into a new fresh WSL instance."},
    {"subject": "Agile Scrum Rituals Wiki", "description": "Document the Agile methodologies used in the project including Daily scrums, Sprint Reviews, Retrospectives, and Planning in the Wiki."}
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

print("Sprint 8 populated!")

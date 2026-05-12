import requests
import urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = 'https://192.168.130.161/taiga/api/v1'

auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

print("Fetching Sprints...")
milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
sprint12 = next((m for m in milestones if m['name'] == 'Sprint 12'), None)

if not sprint12:
    print("Sprint 12 not found, creating it...")
    payload = {
        "project": proj_id,
        "name": "Sprint 12",
        "estimated_start": datetime.now().strftime('%Y-%m-%d'),
        "estimated_finish": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    }
    sprint12 = requests.post(f'{base_url}/milestones', json=payload, headers=headers, verify=False).json()
    
sprint_id = sprint12['id']
print(f"Sprint 12 ID: {sprint_id}")

stories = [
    {"subject": "AI Meal Plan PDF Generation", "description": "Implement FPDF2 script to intercept the Ollama Markdown output, parse the tables, and provide a downloadable PDF artifact for dietitians to hand out."},
    {"subject": "Health Profile Input Constraints", "description": "Refactor the EAV profile tab to use specific drop-down menus instead of text-inputs to strictly enforce the clinical backend flags (Kosher, Halal, Diabetes)."}
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

print("Sprint 12 populated!")

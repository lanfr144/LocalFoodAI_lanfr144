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
sprint11 = next((m for m in milestones if m['name'] == 'Sprint 11'), None)

if not sprint11:
    print("Sprint 11 not found, creating it...")
    payload = {
        "project": proj_id,
        "name": "Sprint 11",
        "estimated_start": datetime.now().strftime('%Y-%m-%d'),
        "estimated_finish": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    }
    sprint11 = requests.post(f'{base_url}/milestones', json=payload, headers=headers, verify=False).json()
    
sprint_id = sprint11['id']
print(f"Sprint 11 ID: {sprint_id}")

stories = [
    {"subject": "Pre-Emptive Database Cleaning via Upsert", "description": "Rewrite ingestion logic to use COALESCE and ON DUPLICATE KEY UPDATE to clean massive CSV dataset without requiring GROUP BY in the app layer."},
    {"subject": "Cascaded Search Logic & Nutrient Selectors", "description": "Update Plate Builder to allow scoped search (Name vs Ingredients) and sort results dynamically by nutrient richness (Iron, Vitamin C)."},
    {"subject": "Food Scale Conversion Expansion", "description": "Update unit_converter.py to natively support extra-large, large, medium, and small egg sizing and generic food scales."},
    {"subject": "Self-Detaching NOHUP Ingestion Sync", "description": "Refactor data_sync.sh to proactively request sudo authentication upfront and detach the process to survive SSH drops."}
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

print("Sprint 11 populated!")

# Get Closed status IDs
us_statuses = requests.get(f'{base_url}/userstory-statuses?project={proj_id}', headers=headers, verify=False).json()
task_statuses = requests.get(f'{base_url}/task-statuses?project={proj_id}', headers=headers, verify=False).json()

closed_us_status = next((s['id'] for s in us_statuses if s['is_closed']), None)
closed_task_status = next((s['id'] for s in task_statuses if s['is_closed']), None)

# Update User Stories
us_list = requests.get(f'{base_url}/userstories?project={proj_id}&milestone={sprint_id}', headers=headers, verify=False).json()
for us in us_list:
    payload = {"status": closed_us_status, "version": us['version']}
    requests.patch(f'{base_url}/userstories/{us["id"]}', json=payload, headers=headers, verify=False)
    print(f"Closed User Story: {us['subject']}")

# Update Tasks
tasks = requests.get(f'{base_url}/tasks?project={proj_id}&milestone={sprint_id}', headers=headers, verify=False).json()
for task in tasks:
    payload = {"status": closed_task_status, "version": task['version']}
    requests.patch(f'{base_url}/tasks/{task["id"]}', json=payload, headers=headers, verify=False)
    print(f"Closed Task: {task['subject']}")

print("Sprint 11 successfully closed!")

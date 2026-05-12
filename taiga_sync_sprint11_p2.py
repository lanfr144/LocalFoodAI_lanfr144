import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

print("Fetching Sprints...")
milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
sprint11 = next((m for m in milestones if m['name'] == 'Sprint 11'), None)

if not sprint11:
    print("Sprint 11 not found! Exiting.")
    exit(1)
    
sprint_id = sprint11['id']
print(f"Sprint 11 ID: {sprint_id}")

stories = [
    {"subject": "AI Dietary Restriction SQL Enforcement", "description": "Dynamically map User EAV profiles (Diabetes, Kosher, Halal, Christian) directly to SQL WHERE clauses to enforce medical boundaries before AI generation."},
    {"subject": "Zabbix Database Ingestion Telemetry", "description": "Build python script to fetch exact row counts from products_core and push SNMP traps to Zabbix Server 192.168.130.170."}
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

print("New User Stories populated!")

# Get Closed status IDs
us_statuses = requests.get(f'{base_url}/userstory-statuses?project={proj_id}', headers=headers, verify=False).json()
task_statuses = requests.get(f'{base_url}/task-statuses?project={proj_id}', headers=headers, verify=False).json()

closed_us_status = next((s['id'] for s in us_statuses if s['is_closed']), None)
closed_task_status = next((s['id'] for s in task_statuses if s['is_closed']), None)

# Update User Stories
us_list = requests.get(f'{base_url}/userstories?project={proj_id}&milestone={sprint_id}', headers=headers, verify=False).json()
for us in us_list:
    if us['status'] != closed_us_status:
        payload = {"status": closed_us_status, "version": us['version']}
        requests.patch(f'{base_url}/userstories/{us["id"]}', json=payload, headers=headers, verify=False)
        print(f"Closed User Story: {us['subject']}")

# Update Tasks
tasks = requests.get(f'{base_url}/tasks?project={proj_id}&milestone={sprint_id}', headers=headers, verify=False).json()
for task in tasks:
    if task['status'] != closed_task_status:
        payload = {"status": closed_task_status, "version": task['version']}
        requests.patch(f'{base_url}/tasks/{task["id"]}', json=payload, headers=headers, verify=False)
        print(f"Closed Task: {task['subject']}")

print("Sprint 11 successfully closed!")

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

print("Fetching Sprints...")
milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
sprint12 = next((m for m in milestones if m['name'] == 'Sprint 12'), None)

if not sprint12:
    print("Sprint 12 not found! Exiting.")
    exit(1)
    
sprint_id = sprint12['id']

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

print("Sprint 12 successfully closed!")

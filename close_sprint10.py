import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}

proj_id = 21

# Get Closed status IDs
us_statuses = requests.get(f'{base_url}/userstory-statuses?project={proj_id}', headers=headers, verify=False).json()
task_statuses = requests.get(f'{base_url}/task-statuses?project={proj_id}', headers=headers, verify=False).json()

closed_us_status = next((s['id'] for s in us_statuses if s['is_closed']), None)
closed_task_status = next((s['id'] for s in task_statuses if s['is_closed']), None)

# 2. Find Sprint 10
milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
sprint10 = next((m for m in milestones if m['name'] == 'Sprint 10'), None)

if sprint10:
    print(f"Closing User Stories and Tasks in Sprint 10 (ID: {sprint10['id']})")
    
    # Update User Stories
    us_list = sprint10.get('user_stories', [])
    for us in us_list:
        payload = {"status": closed_us_status, "version": us['version']}
        requests.patch(f'{base_url}/userstories/{us["id"]}', json=payload, headers=headers, verify=False)
        print(f"Closed User Story: {us['subject']} (ID: {us['id']})")
    
    # Update Tasks
    tasks = requests.get(f'{base_url}/tasks?project={proj_id}&milestone={sprint10["id"]}', headers=headers, verify=False).json()
    for task in tasks:
        payload = {"status": closed_task_status, "version": task['version']}
        requests.patch(f'{base_url}/tasks/{task["id"]}', json=payload, headers=headers, verify=False)
        print(f"Closed Task: {task['subject']} (ID: {task['id']})")
else:
    print("Sprint 10 not found.")

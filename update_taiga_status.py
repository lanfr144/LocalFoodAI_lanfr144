import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = 'https://192.168.130.161/taiga/api/v1'

def close_sprint_tasks():
    try:
        # Authenticate
        auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
        headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
        proj_id = 21

        # 1. Get Milestone (Sprint 9)
        milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
        sprint9 = next((m for m in milestones if m['name'] == 'Sprint 9'), None)
        
        if not sprint9:
            print("Sprint 9 not found!")
            return
            
        sprint_id = sprint9['id']
        
        # 2. Get 'Closed' Task Status ID
        statuses = requests.get(f'{base_url}/task-statuses?project={proj_id}', headers=headers, verify=False).json()
        closed_status = next((s for s in statuses if s['is_closed']), None)
        if not closed_status:
            print("Could not find a 'Closed' task status for the project.")
            return
        
        closed_status_id = closed_status['id']
        print(f"Found Closed Status ID: {closed_status_id}")

        # 3. Get all tasks for Sprint 9
        tasks = requests.get(f'{base_url}/tasks?project={proj_id}&milestone={sprint_id}', headers=headers, verify=False).json()
        
        # 4. Close Tasks
        for task in tasks:
            if task['status'] != closed_status_id:
                payload = {
                    "status": closed_status_id,
                    "version": task['version']
                }
                res = requests.patch(f'{base_url}/tasks/{task["id"]}', json=payload, headers=headers, verify=False).json()
                print(f"Closed Task TG-{task['ref']}: {task['subject']}")
            else:
                print(f"Task TG-{task['ref']} already closed.")
                
        print("Successfully updated all Taiga tasks to Closed!")
        
    except Exception as e:
        print(f"Error updating Taiga: {e}")

if __name__ == "__main__":
    close_sprint_tasks()

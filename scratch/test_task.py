import requests
import urllib3
urllib3.disable_warnings()

auth = requests.post('https://192.168.130.161/taiga/api/v1/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'your_db_password_here'}, verify=False).json()
h = {'Authorization': f'Bearer {auth["auth_token"]}'}

# Let's get the list of tasks to see a valid ID
tasks = requests.get('https://192.168.130.161/taiga/api/v1/tasks?project=21', headers=h, verify=False).json()
if tasks:
    task_id = tasks[0]['id']
    task_ref = tasks[0]['ref']
    print(f"Task ID: {task_id}, Ref: {task_ref}")
    
    # Get details
    detail = requests.get(f'https://192.168.130.161/taiga/api/v1/tasks/{task_id}', headers=h, verify=False).json()
    print("Description in list:", tasks[0].get('description'))
    print("Description in detail:", detail.get('description'))

import requests
import urllib3
urllib3.disable_warnings()

auth = requests.post(
    'https://192.168.130.161/taiga/api/v1/auth', 
    json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, 
    verify=False
).json()

headers = {'Authorization': f'Bearer {auth["auth_token"]}'}

for pid in [18, 21]:
    try:
        tasks = requests.get(f'https://192.168.130.161/taiga/api/v1/tasks?project={pid}', headers=headers, verify=False).json()
        if isinstance(tasks, list):
            for t in tasks:
                if str(t.get('ref')) in ['15', '16', '17', '18', '20', '21', '22']:
                    status_id = t.get('status')
                    status_info = requests.get(f'https://192.168.130.161/taiga/api/v1/task-statuses/{status_id}', headers=headers, verify=False).json() if status_id else {}
                    print(f'Ref: TG-{t.get("ref")}, Status: {status_info.get("name", "Unknown")}, Subject: {t.get("subject")}')
    except Exception as e:
        print(f"Error fetching project {pid}: {e}")

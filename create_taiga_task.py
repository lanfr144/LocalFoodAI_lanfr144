import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
sprint8 = next((m for m in milestones if m['name'] == 'Sprint 8'), None)
sprint_id = sprint8['id'] if sprint8 else None

payload = {"project": proj_id, "subject": "Deep System Overhaul Phase 3", "description": "Fix Clinical Search Crash, Plate Builder UI, and AI Meal Planner JSON parsing.", "milestone": sprint_id}
res = requests.post(f'{base_url}/userstories', json=payload, headers=headers, verify=False).json()
us_id = res['id']
print(f"Created US: TG-{res['ref']}")

t_payload = {"project": proj_id, "subject": "Execute Phase 3 Overhaul", "user_story": us_id, "milestone": sprint_id}
t_res = requests.post(f'{base_url}/tasks', json=t_payload, headers=headers, verify=False).json()
print(f"Created Task: TG-{t_res['ref']}")

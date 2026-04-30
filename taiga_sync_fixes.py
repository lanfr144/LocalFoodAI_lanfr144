import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

# Fetch sprint 8
milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
sprint8 = next((m for m in milestones if m['name'] == 'Sprint 8'), None)
sprint_id = sprint8['id'] if sprint8 else None

if sprint_id:
    payload = {
        "project": proj_id,
        "subject": "Sprint 8 Final Bug Fixes & Polish",
        "description": "Implemented dynamic Help Sections in UI, upgraded LLM to Llama3 with strict anti-hallucination prompts, dynamic Pandas Styler limit caps, MyPlate bug fixes, and null-macro product filters.",
        "milestone": sprint_id
    }
    res = requests.post(f'{base_url}/userstories', json=payload, headers=headers, verify=False)
    if res.status_code == 201:
        us = res.json()
        print(f"Created Fixes US: {us['subject']}")
        t_payload = {"project": proj_id, "subject": "Execute Bug Fixes", "user_story": us['id'], "milestone": sprint_id}
        requests.post(f'{base_url}/tasks', json=t_payload, headers=headers, verify=False)
    else:
        print(f"Failed US: {res.text}")

import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}

proj_id = 21

print("--- TAIGA AUDIT REPORT ---")
# 1. Sprints Check
milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
print(f"Total Sprints: {len(milestones)}")
for m in milestones:
    us_list = m.get('user_stories', [])
    if not us_list:
        print(f"WARNING: Sprint '{m['name']}' has NO User Stories.")
    else:
        # Get tasks for sprint
        tasks = requests.get(f'{base_url}/tasks?project={proj_id}&milestone={m["id"]}', headers=headers, verify=False).json()
        if not tasks:
            print(f"WARNING: Sprint '{m['name']}' has User Stories but NO Tasks.")

# 2. User Stories Check
us_all = requests.get(f'{base_url}/userstories?project={proj_id}', headers=headers, verify=False).json()
for us in us_all:
    tasks = requests.get(f'{base_url}/tasks?project={proj_id}&user_story={us["id"]}', headers=headers, verify=False).json()
    if not tasks:
        print(f"WARNING: User Story '{us['subject']}' (ID: {us['id']}) has NO Tasks.")

# 3. Wiki Check
wiki_pages = requests.get(f'{base_url}/wiki?project={proj_id}', headers=headers, verify=False).json()
print("\n--- WIKI PAGES ---")
for wp in wiki_pages:
    print(f"- {wp['slug']}")


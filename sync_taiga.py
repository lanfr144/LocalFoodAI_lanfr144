import os
import requests
import urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Authenticate
base_url = 'https://192.168.130.161/taiga/api/v1'
auth_url = f'{base_url}/auth'
auth = requests.post(auth_url, json={'type': 'normal', 'username': 'lanfr1904@outlook.com', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

# 1. Sync Milestones (Sprints 1-8)
print("Syncing Sprints/Milestones...")
existing_m_res = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
existing_sprints = {m['name']: m for m in existing_m_res}

start_date = datetime(2026, 4, 16)
for i in range(1, 9):
    sprint_name = f"Sprint {i}"
    sprint_start = start_date + timedelta(weeks=i-1)
    sprint_end = sprint_start + timedelta(days=6)
    
    if sprint_name not in existing_sprints:
        payload = {
            "project": proj_id,
            "name": sprint_name,
            "estimated_start": sprint_start.strftime('%Y-%m-%d'),
            "estimated_finish": sprint_end.strftime('%Y-%m-%d')
        }
        res = requests.post(f'{base_url}/milestones', json=payload, headers=headers, verify=False)
        if res.status_code == 201:
            print(f"Created {sprint_name}")
        else:
            print(f"Failed to create {sprint_name}: {res.text}")

# 2. Sync Wiki
print("\nSyncing Wiki pages...")
for filename in os.listdir('taiga_wiki'):
    if not filename.endswith('.md'):
        continue
    
    filepath = os.path.join('taiga_wiki', filename)
    with open(filepath, 'r') as f:
        content = f.read()
        
    slug = filename.replace('.md', '').lower().replace('_', '-')
    
    # Check if exists
    res = requests.get(f'{base_url}/wiki/by_slug?slug={slug}&project={proj_id}', headers=headers, verify=False)
    if res.status_code == 200:
        # Update
        page_id = res.json()['id']
        version = res.json()['version']
        payload = {
            "project": proj_id,
            "slug": slug,
            "content": content,
            "version": version
        }
        update_res = requests.put(f'{base_url}/wiki/{page_id}', json=payload, headers=headers, verify=False)
        print(f"Updated wiki '{slug}' (status {update_res.status_code})")
        if update_res.status_code != 200:
            print(update_res.text)
    else:
        # Create
        payload = {
            "project": proj_id,
            "slug": slug,
            "content": content
        }
        create_res = requests.post(f'{base_url}/wiki', json=payload, headers=headers, verify=False)
        print(f"Created wiki '{slug}' (status {create_res.status_code})")
        if create_res.status_code != 201:
            print(create_res.text)

print("\nDone syncing to Taiga Local Food AI project!")

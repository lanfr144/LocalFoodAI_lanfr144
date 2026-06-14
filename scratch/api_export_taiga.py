import requests
import urllib3
import os
import json

urllib3.disable_warnings()

TAIGA_USER = os.environ.get('TAIGA_USER', 'FrancoisLange')
TAIGA_PASS = os.environ.get('TAIGA_PASS', 'your_db_password_here')
base_url = 'https://192.168.130.161/taiga/api/v1'

def main():
    print("Logging into Taiga...")
    auth_resp = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False)
    if auth_resp.status_code != 200:
        print("Auth failed!")
        return
        
    auth = auth_resp.json()
    headers = {
        'Authorization': f'Bearer {auth["auth_token"]}', 
        'Content-Type': 'application/json',
        'x-disable-pagination': 'true'
    }
    project_id = 21
    
    print("Fetching project details...")
    project = requests.get(f'{base_url}/projects/{project_id}', headers=headers, verify=False).json()
    
    print("Fetching sprints (milestones)...")
    sprints = requests.get(f'{base_url}/milestones?project={project_id}', headers=headers, verify=False).json()
    
    print("Fetching user stories...")
    user_stories = requests.get(f'{base_url}/userstories?project={project_id}', headers=headers, verify=False).json()
    
    print("Fetching tasks...")
    tasks = requests.get(f'{base_url}/tasks?project={project_id}', headers=headers, verify=False).json()
    
    print("Fetching wiki pages...")
    wikis = requests.get(f'{base_url}/wiki?project={project_id}', headers=headers, verify=False).json()
    
    print("Fetching issues...")
    issues = requests.get(f'{base_url}/issues?project={project_id}', headers=headers, verify=False).json()
    
    export_data = {
        "project": project,
        "sprints": sprints,
        "user_stories": user_stories,
        "tasks": tasks,
        "wiki_pages": wikis,
        "issues": issues
    }
    
    out_path = r'c:\Users\lanfr144\Documents\DOPRO1\Antigravity\taiga_export.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
        
    print(f"API Taiga Export saved successfully to {out_path}!")

if __name__ == '__main__':
    main()

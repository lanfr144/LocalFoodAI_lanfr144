import requests
import urllib3
import os
import sys

urllib3.disable_warnings()
sys.stdout.reconfigure(encoding='utf-8')

TAIGA_USER = os.environ.get('TAIGA_USER', 'FrancoisLange')
TAIGA_PASS = os.environ.get('TAIGA_PASS', 'your_db_password_here')
base_url = 'https://192.168.130.161/taiga/api/v1'

def main():
    print("Connecting to Taiga...")
    auth_resp = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False)
    if auth_resp.status_code != 200:
        print("Auth failed!")
        return
        
    auth = auth_resp.json()
    headers = {
        'Authorization': f'Bearer {auth["auth_token"]}', 
        'Content-Type': 'application/json'
    }
    project_id = 21

    # Fetch current project details
    print("Fetching current project details...")
    p = requests.get(f'{base_url}/projects/{project_id}', headers=headers, verify=False).json()
    print(f"Current project name: '{p['name']}'")

    # Update project name to LocalFoodAI_lanfr144
    new_name = "LocalFoodAI_lanfr144"
    print(f"Renaming project in Taiga to '{new_name}'...")
    
    # Check current version
    version = p.get('version', 1)
    
    payload = {
        "name": new_name,
        "version": version
    }
    
    patch_resp = requests.patch(f'{base_url}/projects/{project_id}', json=payload, headers=headers, verify=False)
    if patch_resp.status_code == 200:
        updated_p = patch_resp.json()
        print("Project successfully renamed!")
        print(f"New project name: '{updated_p['name']}'")
        print(f"New project slug: '{updated_p['slug']}'")
    else:
        print(f"Failed to rename project: {patch_resp.status_code}")
        print(patch_resp.text)

if __name__ == '__main__':
    main()

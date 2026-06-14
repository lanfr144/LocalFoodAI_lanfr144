import requests
import urllib3
import sys

urllib3.disable_warnings()
sys.stdout.reconfigure(encoding='utf-8')

TAIGA_USER = 'FrancoisLange'
TAIGA_PASS = 'your_db_password_here'
base_url = 'https://192.168.130.161/taiga/api/v1'

def main():
    print("Connecting to Taiga...")
    auth_resp = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False)
    if auth_resp.status_code != 200:
        print("Auth failed!")
        return
        
    auth = auth_resp.json()
    headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json', 'x-disable-pagination': 'true'}
    project_id = 21

    # 1. Close all user stories
    print("\n--- 1. Closing User Stories ---")
    us_resp = requests.get(f'{base_url}/userstories?project={project_id}', headers=headers, verify=False).json()
    for us in us_resp:
        # Done status is ID 125
        if us['status'] != 125:
            print(f"Closing User Story {us['ref']}: {us['subject']}...")
            patch = {"status": 125, "version": us['version']}
            requests.patch(f"{base_url}/userstories/{us['id']}", json=patch, headers=headers, verify=False)
        else:
            print(f"User Story {us['ref']}: {us['subject']} is already Done.")

    # 2. Close all tasks
    print("\n--- 2. Closing Tasks ---")
    tasks_resp = requests.get(f'{base_url}/tasks?project={project_id}', headers=headers, verify=False).json()
    for t in tasks_resp:
        # Closed status is ID 104
        if t['status'] != 104:
            print(f"Closing Task #{t['ref']} ({t['id']}): {t['subject']}...")
            patch = {"status": 104, "version": t['version']}
            requests.patch(f"{base_url}/tasks/{t['id']}", json=patch, headers=headers, verify=False)
        else:
            print(f"Task #{t['ref']}: {t['subject']} is already Closed.")

    # 3. Close all issues
    print("\n--- 3. Closing Issues ---")
    issues_resp = requests.get(f'{base_url}/issues?project={project_id}', headers=headers, verify=False).json()
    for issue in issues_resp:
        # Closed status is ID 144
        if issue['status'] != 144:
            print(f"Closing Issue #{issue['ref']}: {issue['subject']}...")
            patch = {"status": 144, "version": issue['version']}
            requests.patch(f"{base_url}/issues/{issue['id']}", json=patch, headers=headers, verify=False)
        else:
            print(f"Issue #{issue['ref']}: {issue['subject']} is already Closed.")

    print("\nTaiga cleanup completed successfully!")

if __name__ == '__main__':
    main()

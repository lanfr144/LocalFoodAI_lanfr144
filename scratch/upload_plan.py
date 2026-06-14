import requests
import urllib3
import os

urllib3.disable_warnings()

TAIGA_USER = os.environ.get('TAIGA_USER', 'FrancoisLange')
TAIGA_PASS = os.environ.get('TAIGA_PASS', 'your_db_password_here')
base_url = 'https://192.168.130.161/taiga/api/v1'
project_id = 21
us_id = 281  # ID of the new User Story

def main():
    print("Connecting to Taiga...")
    auth_resp = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False)
    if auth_resp.status_code != 200:
        print("Auth failed!")
        return
        
    auth = auth_resp.json()
    headers = {
        'Authorization': f'Bearer {auth["auth_token"]}'
    }
    
    plan_path = r"C:\Users\lanfr144\.gemini\antigravity-ide\brain\74c205dc-e2c0-4179-9849-9d8dda480c08\implementation_plan.md"
    if not os.path.exists(plan_path):
        print(f"Error: Implementation plan not found at {plan_path}")
        return
        
    # 1. Attach to User Story
    print(f"Uploading implementation_plan.md to User Story {us_id}...")
    with open(plan_path, 'rb') as f:
        files = {'attached_file': ('implementation_plan.md', f, 'text/markdown')}
        data = {'project': project_id, 'object_id': us_id}
        resp = requests.post(f'{base_url}/userstories/attachments', data=data, files=files, headers=headers, verify=False)
        if resp.status_code == 201:
            print("Successfully attached implementation plan to User Story!")
        else:
            print(f"Failed to attach to User Story: {resp.status_code} {resp.text}")
            
    # 2. Fetch Tasks under this US and attach to each
    tasks = requests.get(f'{base_url}/tasks?user_story={us_id}', headers={'Authorization': f'Bearer {auth["auth_token"]}', 'x-disable-pagination': 'true'}, verify=False).json()
    for task in tasks:
        t_id = task['id']
        t_subject = task['subject']
        print(f"Uploading implementation_plan.md to Task '{t_subject}' (ID: {t_id})...")
        with open(plan_path, 'rb') as f:
            files = {'attached_file': ('implementation_plan.md', f, 'text/markdown')}
            data = {'project': project_id, 'object_id': t_id}
            resp = requests.post(f'{base_url}/tasks/attachments', data=data, files=files, headers=headers, verify=False)
            if resp.status_code == 201:
                print(f"Successfully attached implementation plan to Task '{t_subject}'!")
            else:
                print(f"Failed to attach to Task '{t_subject}': {resp.status_code} {resp.text}")
                
    print("Attachment operations completed.")

if __name__ == '__main__':
    main()

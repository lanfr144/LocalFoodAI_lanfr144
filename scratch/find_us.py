import requests
import urllib3
import os

urllib3.disable_warnings()

TAIGA_USER = os.environ.get('TAIGA_USER', 'FrancoisLange')
TAIGA_PASS = os.environ.get('TAIGA_PASS', 'your_db_password_here')
base_url = 'https://192.168.130.161/taiga/api/v1'
project_id = 21

def main():
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
    
    us = requests.get(f'{base_url}/userstories?project={project_id}', headers=headers, verify=False).json()
    print("User Stories:")
    for u in us:
        print(f" - [{u['ref']}] (ID: {u['id']}): {u['subject']}")
        
if __name__ == '__main__':
    main()

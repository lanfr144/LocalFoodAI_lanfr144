import requests
import urllib3
import os

urllib3.disable_warnings()

TAIGA_USER = os.environ.get('TAIGA_USER', 'FrancoisLange')
TAIGA_PASS = os.environ.get('TAIGA_PASS', 'your_db_password_here')
base_url = 'https://192.168.130.161/taiga/api/v1'

def main():
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
    
    p = requests.get(f'{base_url}/projects/{project_id}', headers=headers, verify=False).json()
    print("Project ID:", p['id'])
    print("Project Name:", p['name'])
    print("Project Slug:", p['slug'])
    print("Project Description:", p.get('description'))
    
if __name__ == '__main__':
    main()

import requests
import urllib3
import os

urllib3.disable_warnings()

TAIGA_USER = 'FrancoisLange'
TAIGA_PASS = 'your_db_password_here'
base_url = 'https://192.168.130.161/taiga/api/v1'
project_id = 21

auth_resp = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False)
auth = auth_resp.json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json', 'x-disable-pagination': 'true'}

user_stories = requests.get(f'{base_url}/userstories?project={project_id}', headers=headers, verify=False).json()
us = next((u for u in user_stories if u['ref'] == 203 or 'US-203' in u['subject'] or '203' in u['subject']), None)

if us:
    print("US ID:", us['id'])
    print("Subject:", us['subject'])
    print("Description:\n", us.get('description', ''))
else:
    print("US-203 not found!")

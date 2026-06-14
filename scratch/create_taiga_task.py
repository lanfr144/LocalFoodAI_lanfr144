import requests
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()
urllib3.disable_warnings()

TAIGA_USER = os.environ.get('TAIGA_USER')
TAIGA_PASS = os.environ.get('TAIGA_PASS')

base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False).json()
h = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}

project_id = 21

payload = {
    "project": project_id,
    "subject": "Configure Zabbix Alerting (Discord & Email) for Downtime & Slow Performance"
}

r = requests.post(f'{base_url}/tasks', json=payload, headers=h, verify=False)
if r.status_code == 201:
    data = r.json()
    print(f"Created Task TG-{data['ref']}")
else:
    print(f"Failed to create task: {r.status_code} {r.text}")

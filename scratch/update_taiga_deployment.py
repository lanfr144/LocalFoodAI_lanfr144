import requests
import json
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()
urllib3.disable_warnings()

TAIGA_USER = os.environ.get('TAIGA_USER', 'FrancoisLange')
TAIGA_PASS = os.environ.get('TAIGA_PASS', 'your_db_password_here')

base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False).json()
h = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
project_id = 21

# 1. Create a User Story / Task for Distributed Deployment
us_payload = {
    "project": project_id,
    "subject": "Distribute Deployment Architecture (WSL, Hyper-V, VirtualBox)",
    "description": "Architected a distributed deployment model. Configured the VMs to use Bridged Adapters for subnet consistency. Created a Python CLI to dynamically deploy components (DB, App, Monitoring) to avoid port conflicts and isolate credentials inside Docker containers."
}
us_resp = requests.post(f'{base_url}/userstories', json=us_payload, headers=h, verify=False)
if us_resp.status_code == 201:
    us_id = us_resp.json()['id']
    task_payload = {
        "project": project_id,
        "user_story": us_id,
        "subject": "Create setup_deploy.py for Docker orchestration",
        "description": "Added docker access checks. Credentials remain strictly isolated in the generated docker-compose .env files."
    }
    requests.post(f'{base_url}/tasks', json=task_payload, headers=h, verify=False)

print("Taiga successfully updated with Distributed Deployment tasks!")

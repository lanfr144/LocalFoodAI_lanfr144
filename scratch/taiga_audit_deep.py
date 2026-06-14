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
auth_resp = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False)
if auth_resp.status_code != 200:
    print("Auth failed!")
    exit(1)
    
auth = auth_resp.json()
h = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
project_id = 21

print("--- Taiga Audit ---")

# User Stories
us_resp = requests.get(f'{base_url}/userstories?project={project_id}', headers=h, verify=False).json()
print(f"Total User Stories: {len(us_resp)}")
for us in us_resp:
    if not us.get("description"):
        print(f"⚠️ User Story '{us['subject']}' is missing a description!")
    if not us.get("milestone"):
        print(f"⚠️ User Story '{us['subject']}' is not assigned to a Sprint (Milestone)!")

# Tasks
tasks_resp = requests.get(f'{base_url}/tasks?project={project_id}', headers=h, verify=False).json()
print(f"Total Tasks: {len(tasks_resp)}")
for t in tasks_resp:
    if not t.get("description"):
        print(f"⚠️ Task '{t['subject']}' is missing a description!")

# Wiki Pages
wiki_resp = requests.get(f'{base_url}/wiki?project={project_id}', headers=h, verify=False).json()
print(f"Total Wiki Pages: {len(wiki_resp)}")
for w in wiki_resp:
    if not w.get("content"):
         print(f"⚠️ Wiki Page '{w['slug']}' is empty!")

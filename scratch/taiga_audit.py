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
h = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json', 'x-disable-pagination': 'true'}
project_id = 21

out = []

# Sprints (Milestones)
sprints = requests.get(f'{base_url}/milestones?project={project_id}', headers=h, verify=False).json()
out.append("SPRINTS:")
for s in sprints:
    out.append(f" - {s['name']} (Closed: {s['closed']})")

# User Stories
us = requests.get(f'{base_url}/userstories?project={project_id}', headers=h, verify=False).json()
out.append("\nUSER STORIES:")
for u in us:
    sprint_name = "NO SPRINT"
    if u['milestone']:
        sprint_name = next((s['name'] for s in sprints if s['id'] == u['milestone']), "Unknown")
    out.append(f" - [{u['status_extra_info']['name']}] {u['subject']} (Sprint: {sprint_name})")

# Tasks
tasks = requests.get(f'{base_url}/tasks?project={project_id}', headers=h, verify=False).json()
out.append("\nTASKS:")
unassigned_tasks = []
empty_description_tasks = []
no_sprint_tasks = []
no_us_tasks = []

for t in tasks:
    if not t.get('description'):
        empty_description_tasks.append(t)
    if not t.get('user_story'):
        no_us_tasks.append(t)
    if not t.get('milestone'):
        no_sprint_tasks.append(t)
    
    status = t.get('status_extra_info', {}).get('name', 'Unknown')
    us_ref = t.get('user_story_extra_info', {}).get('ref', 'None') if t.get('user_story_extra_info') else 'None'
    sprint = "None"
    if t.get('milestone'):
        sprint = next((s['name'] for s in sprints if s['id'] == t['milestone']), "Unknown")
    
    out.append(f" - TG-{t['ref']} [{status}] {t['subject']} (Sprint: {sprint}, US: {us_ref}, Has Desc: {bool(t.get('description'))})")

out.append("\nPROBLEMS FOUND IN TASKS:")
out.append(f"Tasks without User Story: {len(no_us_tasks)}")
out.append(f"Tasks without Sprint: {len(no_sprint_tasks)}")
out.append(f"Tasks without Description: {len(empty_description_tasks)}")

# Wiki Pages
wikis = requests.get(f'{base_url}/wiki?project={project_id}', headers=h, verify=False).json()
out.append("\nWIKI PAGES:")
for w in wikis:
    out.append(f" - {w['slug']}")

with open('scratch/taiga_audit.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(out))

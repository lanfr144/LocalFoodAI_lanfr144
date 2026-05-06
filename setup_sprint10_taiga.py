import requests
import urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Authenticate
base_url = 'https://192.168.130.161/taiga/api/v1'
auth_url = f'{base_url}/auth'
auth = requests.post(auth_url, json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

print("Fetching Sprints...")
milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
sprint10 = next((m for m in milestones if m['name'] == 'Sprint 10'), None)

if not sprint10:
    print("Sprint 10 not found, creating it...")
    payload = {
        "project": proj_id,
        "name": "Sprint 10",
        "estimated_start": datetime.now().strftime('%Y-%m-%d'),
        "estimated_finish": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    }
    sprint10 = requests.post(f'{base_url}/milestones', json=payload, headers=headers, verify=False).json()
    
sprint_id = sprint10['id']
print(f"Sprint 10 ID: {sprint_id}")

stories = [
    {"subject": "Fix Llama3 Tool Compatibility", "description": "Upgrade local LLM from llama3 to llama3.1 to support the tool calling API required by Streamlit."},
    {"subject": "Resolve MySQL Cartesian Product Explosion", "description": "Identify and fix duplicate `code` entries causing massive JOIN explosions and Streamlit duplicate key crashes."},
    {"subject": "Implement Subquery First Optimization Strategy", "description": "Rewrite application SQL queries to apply MATCH() AGAINST() limits inside a subquery before executing LEFT JOINS, reducing search times to milliseconds."},
    {"subject": "UI Execution Timers", "description": "Add time.time() measurement wrappers around SQL queries and display execution times to the user to monitor application performance."},
    {"subject": "Zabbix Microsoft Teams Alert Integration", "description": "Configure Zabbix Webhook Media Types to post server and application alerts directly to a Microsoft Teams channel."}
]

for s in stories:
    payload = {
        "project": proj_id,
        "subject": s["subject"],
        "description": s["description"],
        "milestone": sprint_id
    }
    res = requests.post(f'{base_url}/userstories', json=payload, headers=headers, verify=False)
    if res.status_code == 201:
        us = res.json()
        print(f"Created US: {us['subject']}")
        
        # Create a task for it
        t_payload = {
            "project": proj_id,
            "subject": f"Execute: {us['subject']}",
            "user_story": us['id'],
            "milestone": sprint_id
        }
        requests.post(f'{base_url}/tasks', json=t_payload, headers=headers, verify=False)
    else:
        print(f"Failed US: {res.text}")

print("Sprint 10 populated!")

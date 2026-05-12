import requests
import urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = 'https://192.168.130.161/taiga/api/v1'

auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

print("Fetching Sprints...")
milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
sprint13 = next((m for m in milestones if m['name'] == 'Sprint 13'), None)

if not sprint13:
    print("Sprint 13 not found, creating it...")
    payload = {
        "project": proj_id,
        "name": "Sprint 13",
        "estimated_start": datetime.now().strftime('%Y-%m-%d'),
        "estimated_finish": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    }
    sprint13 = requests.post(f'{base_url}/milestones', json=payload, headers=headers, verify=False).json()
    
sprint_id = sprint13['id']
print(f"Sprint 13 ID: {sprint_id}")

stories = [
    {"subject": "Deploy Local SearXNG Web Search Tool", "description": "The AI must have a local web search tool that it will use to anonymously gather any info that it does not have in its local database."}
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
        
        # Create tasks
        tasks = ["Inject SearXNG container into docker-compose.yml", "Implement Web Search Heuristic fallback in AI Chat", "Integrate SearXNG API payload parsing with Ollama"]
        for t in tasks:
            t_payload = {
                "project": proj_id,
                "subject": t,
                "user_story": us['id'],
                "milestone": sprint_id
            }
            requests.post(f'{base_url}/tasks', json=t_payload, headers=headers, verify=False)

print("Sprint 13 populated!")

import requests, urllib3
urllib3.disable_warnings()

auth = requests.post(
    'https://192.168.130.161/taiga/api/v1/auth', 
    json={'type': 'normal', 'username': 'lanfr1904@outlook.com', 'password': 'BTSai123'}, 
    verify=False
).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}'}
proj_id = 21

us_payload = {"project": proj_id, "subject": "Sprint 4: Operations & Migrations", "total_points": 5}
new_us = requests.post('https://192.168.130.161/taiga/api/v1/userstories', headers=headers, json=us_payload, verify=False).json()

tasks = ["Create unified PDF presentation for review", "Execute Alembic Database Migration scripting", "Sanitize Ollama Mistral LLM endpoints on .170", "Perform Green Recommendation Engine Demo"]
for t in tasks:
    requests.post('https://192.168.130.161/taiga/api/v1/tasks', headers=headers, json={"project": proj_id, "user_story": new_us['id'], "subject": t}, verify=False)
print("Sprint 4 Filled on Taiga!")

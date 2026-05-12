import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

slug = '260508-daily'
content = """# Daily Scrum 26.05.08

## What was done yesterday?
- Addressed application crashes caused by missing columns (`search_limit`) and tables (`products_core`).
- Discovered that the DB drop destroyed the entire schema temporarily until the offline ingestion recreated it, causing UI crashes.
- Implemented `ON DUPLICATE KEY UPDATE` consolidation logic to fix the duplication explosion that degraded search performance.

## What is the plan for today?
- Ensure the initialization SQL officially defines all vertical partitions (`products_core`, `products_macros`, etc.) so the DB structure exists safely before the offline ingestion completes.
- Lock down LLM model initialization into the Docker network `command` argument to strictly decouple the 1.3GB model download from the Streamlit UI loading phase.
- Finalize Food Scale standardizations (`xl`, `l`, `m`, `s`) in `unit_converter.py`.

## Blockers
- **Data Race Condition**: The LLM model stream download crashed the AI interface when requested immediately on app startup. Fixed by detaching the download to the container orchestrator.
- **Table Missing Error**: Streamlit `app.py` querying `products_core` before Python `to_sql` had a chance to create it. Fixed by explicitly declaring schemas in `init.sql`.
"""

payload = {"project": proj_id, "slug": slug, "content": content}
res = requests.post(f'{base_url}/wiki', json=payload, headers=headers, verify=False)
if res.status_code == 201:
    print("Created 260508-daily page!")
else:
    # Try put
    check_req = requests.get(f'{base_url}/wiki?project={proj_id}&slug={slug}', headers=headers, verify=False).json()
    if len(check_req) > 0:
        page_id = check_req[0]['id']
        version = check_req[0]['version']
        res2 = requests.put(f'{base_url}/wiki/{page_id}', json={"project": proj_id, "slug": slug, "content": content, "version": version}, headers=headers, verify=False)
        print("Updated 260508-daily page!")

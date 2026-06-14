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

print("Authenticating to Taiga...")
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False).json()
h = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
project_id = 21

print("Creating User Story...")
us_payload = {
    "project": project_id,
    "subject": "Migrate to Apache Airflow Supervisor & Zabbix Telemetry",
    "description": "Replaced the legacy bash/cron data ingestion pipeline with a robust Apache Airflow Python DAG. Configured the Zabbix API to automatically attach a Web Scenario to the host to poll the Airflow healthcheck endpoint."
}
us_resp = requests.post(f'{base_url}/userstories', json=us_payload, headers=h, verify=False)

if us_resp.status_code == 201:
    us_id = us_resp.json()['id']
    print(f"Created User Story ID: {us_id}")
    
    task_payload = {
        "project": project_id,
        "user_story": us_id,
        "subject": "Replace data_sync.sh cron with Python DAG and configure Zabbix API health checks.",
        "description": "Added Airflow to docker-compose.yml. Wrote dags/openfoodfacts_ingestion.py. Cleared legacy crontab. Configured Zabbix Web Scenario."
    }
    task_resp = requests.post(f'{base_url}/tasks', json=task_payload, headers=h, verify=False)
    if task_resp.status_code == 201:
        print("Created Task successfully!")
    else:
        print("Error creating task:", task_resp.text)
else:
    print("Error creating User Story:", us_resp.text)

print("Taiga update complete.")

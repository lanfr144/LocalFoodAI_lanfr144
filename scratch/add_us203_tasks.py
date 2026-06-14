import requests
import urllib3
import os

urllib3.disable_warnings()

TAIGA_USER = 'FrancoisLange'
TAIGA_PASS = 'your_db_password_here'
base_url = 'https://192.168.130.161/taiga/api/v1'
project_id = 21
us_id = 280  # US-203 ID

def main():
    print("Connecting to Taiga...")
    auth_resp = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False)
    if auth_resp.status_code != 200:
        print("Auth failed!")
        return
        
    auth = auth_resp.json()
    headers = {
        'Authorization': f'Bearer {auth["auth_token"]}',
        'Content-Type': 'application/json',
        'x-disable-pagination': 'true'
    }
    
    # Get user story details to find the correct milestone (sprint)
    us_resp = requests.get(f'{base_url}/userstories/{us_id}', headers=headers, verify=False)
    if us_resp.status_code != 200:
        print(f"Failed to fetch US-{us_id}")
        return
    us = us_resp.json()
    milestone_id = us.get('milestone')
    print(f"User story '{us['subject']}' is assigned to milestone {milestone_id}")

    tasks_to_add = [
        {
            "subject": "Configure Docker Log Rotation Limits",
            "description": "**Changes**: Configured max-size and max-file parameters inside `docker-compose.yml` to set strict limits on container log file sizes.\n**Why**: Prevents log growth from consuming 100% of host disk space during long-term continuous operations.\n**Commit Comment**: `TG-202: Add log rotation limits to prevent 100% disk usage and optimize container disk footprint.`"
        },
        {
            "subject": "Develop Automated Disaster Recovery Validation Script",
            "description": "**Changes**: Developed a robust automated verification bash script `test_dr.sh` that spins up a sandbox MySQL instance, restores the latest compressed database backup, and validates table counts and content.\n**Why**: To routinely and safely test database recovery readiness without risking production data integrity.\n**Commit Comment**: `TG-203: Deploy automated disaster recovery verification script test_dr.sh in developer sandbox.`"
        },
        {
            "subject": "Tune MySQL Database Buffer Pools and Performance Parameters",
            "description": "**Changes**: Adjusted InnoDB memory sizes, page cache parameters, and query buffers inside `my.cnf` configuration to handle optimized vertical partition sets.\n**Why**: Ensures sub-second execution times (<0.04s) for high-frequency clinical keyword lookups.\n**Commit Comment**: `TG-203: Tune InnoDB memory pools and database parameters inside my.cnf for optimized search scaling.`"
        }
    ]

    # Fetch existing tasks under this user story to avoid duplicates
    existing_tasks = requests.get(f'{base_url}/tasks?user_story={us_id}', headers=headers, verify=False).json()
    existing_subjects = {t['subject'] for t in existing_tasks}

    for task in tasks_to_add:
        subject = task['subject']
        if subject in existing_subjects:
            print(f"Task '{subject}' already exists. Skipping.")
            continue
            
        print(f"Creating task '{subject}'...")
        payload = {
            "project": project_id,
            "user_story": us_id,
            "subject": subject,
            "description": task['description'],
            "status": 104,  # Closed
            "milestone": milestone_id
        }
        
        resp = requests.post(f'{base_url}/tasks', json=payload, headers=headers, verify=False)
        if resp.status_code == 201:
            print(f"Successfully created task '{subject}'!")
        else:
            print(f"Failed to create task '{subject}': {resp.status_code} {resp.text}")

    print("Task addition sequence completed.")

if __name__ == '__main__':
    main()

import requests
import urllib3
import os

urllib3.disable_warnings()

TAIGA_USER = os.environ.get('TAIGA_USER', 'FrancoisLange')
TAIGA_PASS = os.environ.get('TAIGA_PASS', 'your_db_password_here')
base_url = 'https://192.168.130.161/taiga/api/v1'
project_id = 21

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
    
    # 1. Check if the User Story already exists
    existing_us = requests.get(f'{base_url}/userstories?project={project_id}', headers=headers, verify=False).json()
    target_us = None
    subject_text = "Customer requesting a bigger model, more focus on the subject"
    
    for u in existing_us:
        if u['subject'].strip().lower() == subject_text.lower():
            target_us = u
            break
            
    # 2. Get active milestones to find a sprint
    sprints = requests.get(f'{base_url}/milestones?project={project_id}', headers=headers, verify=False).json()
    milestone_id = None
    # Use "Sprint 7: Production Hardening & Handover" if found, or first sprint
    sprint_7 = next((s for s in sprints if "Sprint 7" in s['name']), None)
    if sprint_7:
        milestone_id = sprint_7['id']
        print(f"Target Sprint: {sprint_7['name']} (ID: {milestone_id})")
    elif sprints:
        milestone_id = sprints[0]['id']
        print(f"Target Sprint (fallback): {sprints[0]['name']} (ID: {milestone_id})")
        
    if not target_us:
        print(f"Creating User Story: '{subject_text}'...")
        us_payload = {
            "project": project_id,
            "subject": subject_text,
            "description": "The customer requested upgrading to a larger local LLM (e.g. Qwen2.5-7B) for more precise and focused nutritional reasoning, while keeping calculations structured internally using a scratchpad structure to avoid raw thinking cluttering frontend layouts.",
            "milestone": milestone_id
        }
        res = requests.post(f'{base_url}/userstories', json=us_payload, headers=headers, verify=False)
        if res.status_code == 201:
            target_us = res.json()
            print(f"Successfully created User Story ID {target_us['id']} [Ref: {target_us['ref']}]!")
        else:
            print(f"Failed to create User Story: {res.status_code} {res.text}")
            return
    else:
        print(f"User Story already exists with ID {target_us['id']} [Ref: {target_us['ref']}]")
        
    us_id = target_us['id']
    us_ref = target_us['ref']
    
    # 3. Create the three tasks
    tasks_to_add = [
        {
            "subject": "Task 1: Update local LLM to Qwen2.5 (7B)",
            "description": "Update the local LLM configuration via Ollama to remove llama3.2:3b/1b and implement qwen2.5 (7B), ensuring it fits securely within our CPU and 30 GB RAM limits without exceeding our tight disk space."
        },
        {
            "subject": "Task 2: Refactor backend prompts to utilize <scratchpad> CoT structure",
            "description": "Refactor the Python backend prompts (sys_prompt and task_prompt) to utilize a <scratchpad> XML tag structure for internal Chain of Thought (CoT) calculations, specifically forcing conversions to grams and calorie summation."
        },
        {
            "subject": "Task 3: Implement Python parsing function to strip <scratchpad> block",
            "description": "Implement a Python parsing function (using regex or string splitting) to intercept the LLM's response, strip out the entire <scratchpad> block, and return only the final 5-column Markdown table to the frontend."
        }
    ]
    
    # Fetch existing tasks under this user story
    existing_tasks = requests.get(f'{base_url}/tasks?user_story={us_id}', headers=headers, verify=False).json()
    existing_subjects = {t['subject'] for t in existing_tasks}
    
    for task in tasks_to_add:
        subject = task['subject']
        if subject in existing_subjects:
            print(f"Task '{subject}' already exists. Skipping.")
            continue
            
        print(f"Creating task '{subject}'...")
        task_payload = {
            "project": project_id,
            "user_story": us_id,
            "subject": subject,
            "description": task['description'],
            "milestone": milestone_id
        }
        
        resp = requests.post(f'{base_url}/tasks', json=task_payload, headers=headers, verify=False)
        if resp.status_code == 201:
            print(f"Successfully created task '{subject}' [Ref: {resp.json()['ref']}]!")
        else:
            print(f"Failed to create task '{subject}': {resp.status_code} {resp.text}")

if __name__ == '__main__':
    main()

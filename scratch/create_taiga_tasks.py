import requests
import urllib3
import json

urllib3.disable_warnings()

TAIGA_USER = 'FrancoisLange'
TAIGA_PASS = 'your_db_password_here'
base_url = 'https://192.168.130.161/taiga/api/v1'
project_id = 21

# Mapping of User Story Ref to Task details
TASKS_TO_CREATE = {
    2: {
        "subject": "Configure Easy Cloning and Repository Footprint",
        "description": "**Changes**: Streamlined cloning requirements, configured basic dependencies in requirements.txt, and enabled local execution pathways.\n**Why**: Allows new developers or deployers to clone and stand up the stack in seconds in disconnected networks.\n**Commit Comment**: `TG-2: Repository initialized and cloned dependency footprint stabilized for local standalone setup.`"
    },
    3: {
        "subject": "Implement Secure Local User Authentication & Login UI",
        "description": "**Changes**: Integrated bcrypt password hashing in `app.py`, created the user creation/login panels in Streamlit, and set up the `users` table schema in `init.sql`.\n**Why**: Restricts clinical telemetry and patient profiles to authorized clinicians, enforcing security baselines.\n**Commit Comment**: `TG-3: Implement secure local bcrypt hashing and Streamlit authentication gateway.`"
    },
    4: {
        "subject": "Establish Strict Offline Database Constraints & Boundary Limits",
        "description": "**Changes**: Configured container networks to prevent external connections, routing LLM requests strictly to the local Ollama instance and database.\n**Why**: Guarantees zero data leakage for HIPAA/clinical compliance on personal medical profiles.\n**Commit Comment**: `TG-4: Set strict containerized boundary limits to ensure zero external calls for clinical profiling.`"
    },
    9: {
        "subject": "Configure Ollama Local Orchestration for Llama3.2",
        "description": "**Changes**: Integrated the Ollama REST client into `app.py`, pulling `llama3.2:3b` in the background and managing inference queries locally.\n**Why**: Allows offline medical NLP evaluation without relying on commercial cloud-based LLM platforms.\n**Commit Comment**: `TG-9: Integrate Ollama connection pooling and lightweight model download scripts.`"
    },
    10: {
        "subject": "Construct Interactive Clinical AI Chat Interface",
        "description": "**Changes**: Implemented Streamlit chat interface with custom session state tracking, injecting active dietitian medical profile details into the system prompt.\n**Why**: Enables practitioners to dynamically query nutrient databases via natural language conversation.\n**Commit Comment**: `TG-10: Deploy interactive dietetics chat panel with clinical history parsing.`"
    },
    11: {
        "subject": "Deploy Local RAG-Driven Meal Planner Engine",
        "description": "**Changes**: Set up the `tab_planner` view, formulating a structured dietitian system prompt that enforces strict Markdown tables containing Calories and Protein.\n**Why**: Generates clinically safe, calorie-restricted meal options automatically tailored to patient illnesses/diets.\n**Commit Comment**: `TG-11: Integrate tabular meal planner executing local database subqueries.`"
    },
    12: {
        "subject": "Integrate Local SearXNG Private Search Fallback",
        "description": "**Changes**: Integrated a SearXNG client querying `http://searxng:8080` to search the web if database nutrition data is absent.\n**Why**: Provides supplementary recipes while maintaining absolute user anonymity without commercial tracking search engines.\n**Commit Comment**: `TG-12: Integrate local anonymous SearXNG meta-search fallback.`"
    },
    147: {
        "subject": "Create Comprehensive WSL2 Operator Runbook",
        "description": "**Changes**: Formulated explicit WSL2 mounting, Docker Desktop integration guides, and system configuration commands.\n**Why**: Assists administrators in deploying the Local Food AI environment securely on Windows-based enterprise hosts.\n**Commit Comment**: `TG-147: Finalize WSL2 operator guidelines and networking parameters.`"
    },
    149: {
        "subject": "Establish Scrum Rituals Static Documentation",
        "description": "**Changes**: Generated Sprint Daily, Plan, Retro, and Review markdown pages in `docs/` summarizing the operational milestones.\n**Why**: Logs the continuous improvement metrics and velocity tracking required for capstone reviews.\n**Commit Comment**: `TG-149: Compile Scrum wiki index and daily operational logs.`"
    },
    151: {
        "subject": "Apply Codebase Linter Refactoring and SQL Cleanup",
        "description": "**Changes**: Refactored `app.py` warnings logic, streamlined unit conversions, and optimized MySQL index parameters.\n**Why**: Stabilizes the production release candidate for zero-downtime deployment.\n**Commit Comment**: `TG-151: Apply final refactoring patches to Streamlit application components.`"
    },
    153: {
        "subject": "Implement Resilient Subquery Optimizations & Layout UI",
        "description": "**Changes**: Restructured the UI tab layouts and implemented clinical subquery limiting to prevent Cartesian join overhead in database calls.\n**Why**: Reduces page load latency and handles high concurrent request volumes smoothly.\n**Commit Comment**: `TG-153: Optimize database joins and revamp UI theming using custom HSL values.`"
    },
    155: {
        "subject": "Deploy SNMPv3 Encrypted Traps and Zabbix Templates",
        "description": "**Changes**: Configured custom SNMPv3 traps for `snmp_notifier.py` and provisioned dynamic Zabbix host alerts via the API.\n**Why**: Standardizes telemetry gathering and active error notification across multiple distributed nodes.\n**Commit Comment**: `TG-155: Configure SNMPv3 trap parameters and deploy full Zabbix alert dashboard.`"
    }
}

def main():
    auth_resp = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False)
    if auth_resp.status_code != 200:
        print("Auth failed!")
        return
        
    auth = auth_resp.json()
    headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
    
    # Fetch User Stories to map ref to US ID
    print("Fetching user stories...")
    user_stories = requests.get(f'{base_url}/userstories?project={project_id}', headers=headers, verify=False).json()
    us_ref_to_id = {us['ref']: us['id'] for us in user_stories}
    
    # Fetch existing tasks to avoid duplicates
    print("Fetching existing tasks...")
    existing_tasks = requests.get(f'{base_url}/tasks?project={project_id}', headers=headers, verify=False).json()
    existing_subjects = {t['subject'] for t in existing_tasks}
    
    for ref, task_details in TASKS_TO_CREATE.items():
        if ref not in us_ref_to_id:
            print(f"User story US-{ref} not found!")
            continue
            
        us_id = us_ref_to_id[ref]
        subject = task_details['subject']
        description = task_details['description']
        
        if subject in existing_subjects:
            print(f"Task '{subject}' already exists. Skipping creation.")
            continue
            
        print(f"Creating task '{subject}' for US-{ref}...")
        task_payload = {
            "project": project_id,
            "user_story": us_id,
            "subject": subject,
            "description": description,
            "status": 104 # Closed
        }
        
        resp = requests.post(f'{base_url}/tasks', json=task_payload, headers=headers, verify=False)
        if resp.status_code == 201:
            print(f"Successfully created task for US-{ref}!")
        else:
            print(f"Failed to create task for US-{ref}: {resp.text}")
            
    print("\nTasks creation completed successfully!")

if __name__ == '__main__':
    main()

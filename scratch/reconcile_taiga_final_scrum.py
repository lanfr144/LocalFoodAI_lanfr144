import requests
import urllib3
import os
import sys

urllib3.disable_warnings()
sys.stdout.reconfigure(encoding='utf-8')

TAIGA_USER = os.environ.get('TAIGA_USER', 'FrancoisLange')
TAIGA_PASS = os.environ.get('TAIGA_PASS', 'your_db_password_here')
base_url = 'https://192.168.130.161/taiga/api/v1'

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
    project_id = 21

    # 1. Fetch current Sprints (Milestones) to assign stories and tasks properly
    sprints = requests.get(f'{base_url}/milestones?project={project_id}', headers=headers, verify=False).json()
    # Find Sprint 7 (Production Hardening) or similar, let's use the first active sprint or default to sprint 13
    sprint_13 = next((s for s in sprints if "Sprint 13" in s['name']), None)
    if not sprint_13:
        sprint_13 = sprints[0]
    sprint_13_id = sprint_13['id']

    # 2. Define the 11 restricted user stories
    target_stories_def = {
        1: {
            "subject": "US-1: Create an account and log in securely",
            "desc": "As a user, I want to create an account and log in securely, so that my personal clinical profiles and food lists are protected.",
            "match_keywords": ["account", "login", "auth"]
        },
        2: {
            "subject": "US-2: Get complete nutritional value information on any food",
            "desc": "As a user, I want to get complete nutritional value information on any food (including macro nutrients, minerals, vitamins, amino acids etc.), so that I can audit my dietary intake in detail.",
            "match_keywords": ["nutritional info", "macro", "mineral", "vitamin", "ingest", "pandas", "dynamic rebuild", "database schema"]
        },
        3: {
            "subject": "US-3: Get the full nutritional value overview for a given food combination",
            "desc": "As a user, I want to get the full nutritional value overview for a given food combination by entering their quantities, so that I can see the total impact of a recipe or meal.",
            "match_keywords": ["food combination", "quantities", "overview", "scale conversion"]
        },
        4: {
            "subject": "US-4: Search for specific nutrient content and get a sortable list of all foods",
            "desc": "As a user, I want to search for specific nutrient content and get a sortable list of all foods that contain them, so that I can easily find foods that satisfy my micro/macro targets.",
            "match_keywords": ["search for nutrient", "sortable list"]
        },
        5: {
            "subject": "US-5: Store food combinations in named and editable lists",
            "desc": "As a user, I want to store food combinations in named and editable lists, so that I can save my favorite meals for quick access.",
            "match_keywords": ["store food combinations", "editable list"]
        },
        6: {
            "subject": "US-6: Get menu proposals based on nutritional value and health constraints",
            "desc": "As a user, I want to get menu proposals based on nutritional value targets and health/allergy constraints, so that I can automatically follow a safe, tailored diet.",
            "match_keywords": ["menu proposal", "allergy", "dietary preference", "clinical warning", "pdf", "profiler"]
        },
        7: {
            "subject": "US-7: Freely chat about anything related to nutrition and get competent answers",
            "desc": "As a user, I want to freely chat with a competent clinical AI dietitian, so that I can ask any nutrition-related questions and get expert advice.",
            "match_keywords": ["chat", "nutrition", "dietitian"]
        },
        8: {
            "subject": "US-8: Anonymous private web search tool (SearXNG) integration",
            "desc": "As a system operator, I want the AI to utilize a local private web search tool (SearXNG) for anonymous information retrieval when the local database is insufficient, so that the AI can answer external queries without cloud APIs.",
            "match_keywords": ["web search", "searxng", "anonymous"]
        },
        9: {
            "subject": "US-9: 100% local data privacy (no user data leaves the server)",
            "desc": "As a privacy-focused user, I want all computations and data storage to remain strictly local on the server, so that absolutely no user data leaves the server boundary.",
            "match_keywords": ["privacy", "data leaves", "password rotation", "security"]
        },
        10: {
            "subject": "US-10: Public Git repository with easy cloning support (LocalFoodAI_lanfr144)",
            "desc": "As a developer/student, I want the project to reside in a public, real-time updated repo named LocalFoodAI_lanfr144 with easy cloning support and my teacher as a collaborator, so that anyone can deploy the app effortlessly.",
            "match_keywords": ["git", "cloning", "repo", "collaborator", "runbook", "rituals"]
        },
        11: {
            "subject": "US-11: Local hardware boundary containment on Ubuntu 24.04 VM",
            "desc": "As a system architect, I want the application to run entirely on the provided Ubuntu VM (8 vCPUs, 30 GB RAM) utilizing optimized local LLMs and databases, so that we maximize performance without exceeding physical limits.",
            "match_keywords": ["ubuntu", "hardware", "cpu", "ram", "ollama", "qwen", "mistral", "zabbix", "snmp", "telemetry", "log rotation", "dr testing", "airflow", "mysql", "performance", "cartesian"]
        }
    }

    # 3. Fetch all current user stories to map or create
    stories = requests.get(f'{base_url}/userstories?project={project_id}', headers=headers, verify=False).json()
    print(f"Fetched {len(stories)} current user stories.")
    
    # We will rename the 11 closest existing stories to match our subjects, and delete the rest
    mapped_stories = {} # key: 1..11, value: story object or created story object
    
    # Map the existing stories that already perfectly correspond to our points
    keyword_to_target = {
        "User Account Creation": 1,
        "View Complete Nutritional Info": 2,
        "Combined Nutritional Value Overview": 3,
        "Search for Nutrients": 4,
        "Store and Edit Food": 5,
        "AI Menu Proposals": 6,
        "Chat About Nutrition": 7,
        "Anonymous Web Search": 8,
        "Local Data Privacy": 9,
        "Public Git Repo": 10,
        "Lightweight Local AI": 11
    }
    
    for s in stories:
        subj = s['subject']
        for kw, target_id in keyword_to_target.items():
            if kw in subj:
                mapped_stories[target_id] = s
                print(f"Mapped existing US Ref {s['ref']} '{subj}' to Target US-{target_id}")
                break

    # For any target story not mapped, we'll create a new story
    for target_id, t_def in target_stories_def.items():
        if target_id not in mapped_stories:
            # Let's check if there are other stories we can hijack, or create new
            print(f"Target US-{target_id} not mapped. Creating new user story...")
            payload = {
                "project": project_id,
                "milestone": sprint_13_id,
                "subject": t_def["subject"],
                "description": t_def["desc"],
                "status": 125 # Done status
            }
            res = requests.post(f'{base_url}/userstories', json=payload, headers=headers, verify=False)
            if res.status_code == 201:
                mapped_stories[target_id] = res.json()
                print(f"Successfully created US-{target_id}: '{t_def['subject']}' (ID: {mapped_stories[target_id]['id']})")
            else:
                print(f"Failed to create US-{target_id}: {res.text}")
        else:
            # Update the subject and description of mapped existing story
            s = mapped_stories[target_id]
            t_def = target_stories_def[target_id]
            print(f"Updating existing US Ref {s['ref']} to '{t_def['subject']}'...")
            payload = {
                "subject": t_def["subject"],
                "description": t_def["desc"],
                "version": s["version"],
                "status": 125 # Done status
            }
            res = requests.patch(f'{base_url}/userstories/{s["id"]}', json=payload, headers=headers, verify=False)
            if res.status_code == 200:
                mapped_stories[target_id] = res.json()
                print(f"Successfully updated US-{target_id}")
            else:
                print(f"Failed to update US-{target_id}: {res.text}")

    # Set of target story IDs in Taiga
    target_story_ids = {s['id'] for s in mapped_stories.values()}
    print(f"Target User Story IDs in Taiga: {target_story_ids}")

    # 4. Fetch all tasks to migrate
    tasks = requests.get(f'{base_url}/tasks?project={project_id}', headers=headers, verify=False).json()
    print(f"Fetched {len(tasks)} tasks.")

    # 5. Map tasks to target story IDs
    for t in tasks:
        current_us_id = t.get('user_story')
        current_us_subject = t.get('user_story_extra_info', {}).get('subject', '') if t.get('user_story_extra_info') else ''
        
        # If task is already under one of the 11 target stories, no need to change
        if current_us_id in target_story_ids:
            # Let's ensure it is in closed status
            if t['status'] != 104:
                patch_payload = {"status": 104, "version": t["version"]}
                requests.patch(f'{base_url}/tasks/{t["id"]}', json=patch_payload, headers=headers, verify=False)
            continue
            
        # Determine which target story this task belongs to
        task_subj = t['subject'].lower()
        task_desc = (t.get('description') or '').lower()
        combined_text = task_subj + " " + task_desc + " " + current_us_subject.lower()
        
        assigned_target_id = 11 # Default fallback to Infrastructure
        
        # Check matching keywords
        matched = False
        for target_id, t_def in target_stories_def.items():
            for kw in t_def["match_keywords"]:
                if kw in combined_text:
                    assigned_target_id = target_id
                    matched = True
                    break
            if matched:
                break
                
        target_us = mapped_stories[assigned_target_id]
        print(f"Migrating Task TG-{t['ref']} '{t['subject']}' to US-{assigned_target_id} '{target_us['subject']}'...")
        
        # Patch task to reassign user story and ensure closed status
        patch_payload = {
            "user_story": target_us['id'],
            "status": 104, # Closed status
            "version": t["version"]
        }
        res = requests.patch(f'{base_url}/tasks/{t["id"]}', json=patch_payload, headers=headers, verify=False)
        if res.status_code == 200:
            print(f"  Successfully migrated Task TG-{t['ref']}")
        else:
            print(f"  Failed to migrate Task TG-{t['ref']}: {res.text}")

    # 6. Delete all other purely technical user stories
    all_stories = requests.get(f'{base_url}/userstories?project={project_id}', headers=headers, verify=False).json()
    deleted_count = 0
    for s in all_stories:
        if s['id'] not in target_story_ids:
            print(f"Deleting technical user story Ref {s['ref']} '{s['subject']}'...")
            res = requests.delete(f'{base_url}/userstories/{s["id"]}', headers=headers, verify=False)
            if res.status_code in [200, 204]:
                print(f"  Successfully deleted US Ref {s['ref']}")
                deleted_count += 1
            else:
                print(f"  Failed to delete US Ref {s['ref']}: {res.text}")
                
    print(f"Reconciliation completed successfully! Deleted {deleted_count} technical stories.")

if __name__ == '__main__':
    main()

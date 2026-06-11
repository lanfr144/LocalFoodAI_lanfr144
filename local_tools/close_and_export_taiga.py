#!/usr/bin/env python
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import requests
import json
import sys
from dotenv import load_dotenv
import urllib3

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Load local environment configuration
load_dotenv()

TAIGA_URL = os.getenv("TAIGA_URL")
if TAIGA_URL:
    TAIGA_API_URL = f"{TAIGA_URL.rstrip('/')}/api/v1"
    TAIGA_USERNAME = os.getenv("TAIGA_USER", "FrancoisLange")
    TAIGA_PASSWORD = os.getenv("TAIGA_PASS")
    PROJECT_ID = os.getenv("TAIGA_PROJECT_ID", "21")
else:
    TAIGA_API_URL = os.getenv("TAIGA_API_URL", "https://api.taiga.io/api/v1")
    TAIGA_USERNAME = os.getenv("TAIGA_USERNAME")
    TAIGA_PASSWORD = os.getenv("TAIGA_PASSWORD")
    PROJECT_ID = os.getenv("TAIGA_PROJECT_ID")

urllib3.disable_warnings()
session = requests.Session()
session.verify = False

def authenticate_taiga():
    print("[INFO] Authenticating with Taiga...")
    payload = {
        "type": "normal",
        "username": TAIGA_USERNAME,
        "password": TAIGA_PASSWORD
    }
    response = session.post(f"{TAIGA_API_URL}/auth", json=payload)
    response.raise_for_status()
    return response.json().get("auth_token")

def get_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def main():
    if not TAIGA_USERNAME or not TAIGA_PASSWORD or not PROJECT_ID:
        print("[ERROR] Missing Taiga credentials in .env")
        sys.exit(1)

    token = authenticate_taiga()
    headers = get_headers(token)

    # 1. Retrieve all User Stories to locate the target one
    print("[INFO] Fetching user stories...")
    r = session.get(f"{TAIGA_API_URL}/userstories?project={PROJECT_ID}", headers=headers)
    r.raise_for_status()
    user_stories = r.json()
    
    target_us_id = None
    target_subject = "As a team, we need enhanced communication and documentation."
    for us in user_stories:
        if us["subject"] == target_subject:
            target_us_id = us["id"]
            break
            
    if not target_us_id and user_stories:
        # Fallback to the first story if the target one isn't found
        target_us_id = user_stories[0]["id"]
        print(f"[WARNING] Target story not found. Using fallback story ID: {target_us_id}")
    elif not target_us_id:
        print("[ERROR] No user stories found in the project.")
        sys.exit(1)
    else:
        print(f"[INFO] Found target user story ID: {target_us_id}")

    # 2. Create the documentation task if it doesn't exist yet
    task_subject = "Create skill directory setup and configuration guide"
    
    # Check if task already exists
    print("[INFO] Checking if documentation task already exists...")
    r = session.get(f"{TAIGA_API_URL}/tasks?project={PROJECT_ID}", headers=headers)
    r.raise_for_status()
    tasks = r.json()
    
    task_exists = False
    for t in tasks:
        if t["subject"] == task_subject:
            task_exists = True
            break
            
    if not task_exists:
        print(f"[INFO] Creating task: '{task_subject}'...")
        task_payload = {
            "subject": task_subject,
            "project": int(PROJECT_ID),
            "user_story": target_us_id
        }
        r = session.post(f"{TAIGA_API_URL}/tasks", json=task_payload, headers=headers)
        r.raise_for_status()
        print("[SUCCESS] Task created successfully!")
        
        # Re-fetch tasks to include the new one
        r = session.get(f"{TAIGA_API_URL}/tasks?project={PROJECT_ID}", headers=headers)
        r.raise_for_status()
        tasks = r.json()
    else:
        print("[INFO] Documentation task already exists.")

    # 3. Fetch and close all tasks
    print(f"[INFO] Closing {len(tasks)} tasks...")
    for t in tasks:
        tid = t["id"]
        # Skip if already closed
        if t.get("status_extra_info", {}).get("is_closed", False) or t.get("is_closed", False):
            print(f"  - Task already closed: {t['subject']}")
            continue
        print(f"  - Closing task: {t['subject']} (ID: {tid}, Version: {t.get('version')})")
        # Try to find the closed status ID dynamically or use a standard close logic
        # In self-hosted Taiga, closed status might have a different ID, so let's check
        # status and set to is_closed.
        closed_status_id = None
        # We can fetch statuses to find one that is_closed
        try:
            statuses_resp = session.get(f"{TAIGA_API_URL}/task-statuses?project={PROJECT_ID}", headers=headers).json()
            closed_status_id = next((s["id"] for s in statuses_resp if s["is_closed"]), None)
        except Exception:
            pass
        if not closed_status_id:
            closed_status_id = 8901961  # Fallback
            
        r = session.patch(f"{TAIGA_API_URL}/tasks/{tid}", json={"status": closed_status_id, "version": t["version"]}, headers=headers)
        if not r.ok:
            print(f"[ERROR] Failed to close task {tid}: {r.text}")
        r.raise_for_status()

    # 4. Close all User Stories
    r = session.get(f"{TAIGA_API_URL}/userstories?project={PROJECT_ID}", headers=headers)
    r.raise_for_status()
    user_stories = r.json()
    
    print(f"[INFO] Closing {len(user_stories)} user stories...")
    for us in user_stories:
        usid = us["id"]
        if us.get("status_extra_info", {}).get("is_closed", False) or us.get("is_closed", False):
            print(f"  - Story already closed: {us['subject']}")
            continue
        print(f"  - Closing story: {us['subject']} (ID: {usid}, Version: {us.get('version')})")
        closed_us_status_id = None
        try:
            statuses_resp = session.get(f"{TAIGA_API_URL}/userstory-statuses?project={PROJECT_ID}", headers=headers).json()
            closed_us_status_id = next((s["id"] for s in statuses_resp if s["is_closed"]), None)
        except Exception:
            pass
        if not closed_us_status_id:
            closed_us_status_id = 10832456  # Fallback
            
        r = session.patch(f"{TAIGA_API_URL}/userstories/{usid}", json={"status": closed_us_status_id, "version": us["version"]}, headers=headers)
        if not r.ok:
            print(f"[ERROR] Failed to close story {usid}: {r.text}")
        r.raise_for_status()

    # 5. Close all Sprints/Milestones
    print("[INFO] Fetching Sprints...")
    r = session.get(f"{TAIGA_API_URL}/milestones?project={PROJECT_ID}", headers=headers)
    r.raise_for_status()
    milestones = r.json()

    print(f"[INFO] Closing {len(milestones)} milestones...")
    for m in milestones:
        mid = m["id"]
        if m["closed"]:
            print(f"  - Milestone already closed: {m['name']}")
            continue
        print(f"  - Closing milestone: {m['name']} (ID: {mid}, Version: {m.get('version')})")
        r = session.patch(f"{TAIGA_API_URL}/milestones/{mid}", json={"closed": True, "version": m.get("version")}, headers=headers)
        if not r.ok:
            print(f"[ERROR] Failed to close milestone {mid}: {r.text}")
        r.raise_for_status()

    # 6. Fetch final state and export to JSON
    print("[INFO] Fetching final project state for export...")
    
    r = session.get(f"{TAIGA_API_URL}/milestones?project={PROJECT_ID}", headers=headers)
    final_milestones = r.json()
    
    r = session.get(f"{TAIGA_API_URL}/userstories?project={PROJECT_ID}", headers=headers)
    final_stories = r.json()
    
    r = session.get(f"{TAIGA_API_URL}/tasks?project={PROJECT_ID}", headers=headers)
    final_tasks = r.json()

    export_data = {
        "project_id": PROJECT_ID,
        "sprints": [
            {
                "id": m["id"],
                "name": m["name"],
                "estimated_start": m["estimated_start"],
                "estimated_finish": m["estimated_finish"],
                "closed": m["closed"]
            } for m in final_milestones
        ],
        "user_stories": [
            {
                "id": us["id"],
                "subject": us["subject"],
                "status_id": us["status"],
                "is_closed": us.get("is_closed", False),
                "milestone": us["milestone"]
            } for us in final_stories
        ],
        "tasks": [
            {
                "id": t["id"],
                "subject": t["subject"],
                "status_id": t["status"],
                "is_closed": t.get("is_closed", False),
                "user_story": t["user_story"]
            } for t in final_tasks
        ]
    }

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    export_path = os.path.join(base_dir, "docs", "taiga_export.json")
    
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=4, ensure_ascii=False)
    print(f"[SUCCESS] Saved export to: {export_path}")

    # Also save to the special taiga directory dump path if it exists
    taiga_dir = os.path.join(base_dir, "taiga")
    if os.path.exists(taiga_dir):
        special_path = os.path.join(taiga_dir, "local-food-ai-1-eab691c0-9c19-4dce-ac66-3b8fade77ef7.json")
        with open(special_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=4, ensure_ascii=False)
        print(f"[SUCCESS] Saved export to: {special_path}")

if __name__ == "__main__":
    main()
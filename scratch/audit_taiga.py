import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = 'https://192.168.130.161/taiga/api/v1'

def audit():
    try:
        auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
        headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
        proj_id = 21

        milestones = requests.get(f'{base_url}/milestones?project={proj_id}', headers=headers, verify=False).json()
        sprint11 = next((m for m in milestones if m['name'] == 'Sprint 11'), None)
        
        if not sprint11:
            print("Sprint 11 not found.")
            return

        sprint_id = sprint11['id']
        print(f"--- SPRINT 11 AUDIT ---")
        
        us_statuses = requests.get(f'{base_url}/userstory-statuses?project={proj_id}', headers=headers, verify=False).json()
        status_map = {s['id']: s['name'] for s in us_statuses}
        
        us_list = requests.get(f'{base_url}/userstories?project={proj_id}&milestone={sprint_id}', headers=headers, verify=False).json()
        
        all_closed = True
        for us in us_list:
            status_name = status_map.get(us['status'], 'Unknown')
            print(f"[US] {us['subject']} - Status: {status_name}")
            if status_name.lower() != 'closed':
                all_closed = False
                
        print(f"Sprint fully closed? {'YES' if all_closed else 'NO'}")

    except Exception as e:
        print(f"Failed to audit Taiga: {e}")

if __name__ == "__main__":
    audit()

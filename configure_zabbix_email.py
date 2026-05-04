import requests
import json
import os

ZABBIX_API_URL = "http://localhost:8081/api_jsonrpc.php"
ZABBIX_USER = "Admin"
ZABBIX_PASSWORD = "zabbix"

def get_email_from_env():
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('ADMIN_EMAIL='):
                    return line.strip().split('=', 1)[1]
    return "lanfr144@gmail.com" # Default fallback

def authenticate():
    payload = {"jsonrpc": "2.0", "method": "user.login", "params": {"user": ZABBIX_USER, "password": ZABBIX_PASSWORD}, "id": 1}
    try:
        response = requests.post(ZABBIX_API_URL, json=payload).json()
        return response.get('result')
    except Exception as e:
        print(f"Error connecting to Zabbix API: {e}")
        return None

def configure_email(auth_token, email_address):
    # 1. Update Admin User (ID 1) Media
    print(f"Configuring Admin user to receive alerts at: {email_address}")
    user_payload = {
        "jsonrpc": "2.0",
        "method": "user.update",
        "params": {
            "userid": "1",
            "medias": [
                {
                    "mediatypeid": "1", # Default Email media type
                    "sendto": [email_address],
                    "active": 0, # Enabled
                    "severity": 63, # All severities
                    "period": "1-7,00:00-24:00"
                }
            ]
        },
        "id": 2,
        "auth": auth_token
    }
    res = requests.post(ZABBIX_API_URL, json=user_payload).json()
    if 'result' in res:
        print("User media successfully updated.")
    else:
        print(f"Failed to update user media: {res}")
        
    # 2. Enable "Report problems to Zabbix administrators" Action
    # Usually ID 2 or 3. Let's find it.
    action_search = {
        "jsonrpc": "2.0",
        "method": "action.get",
        "params": {
            "output": ["actionid", "name"],
            "search": {"name": "Report problems to Zabbix administrators"}
        },
        "id": 3,
        "auth": auth_token
    }
    actions = requests.post(ZABBIX_API_URL, json=action_search).json().get('result', [])
    if actions:
        action_id = actions[0]['actionid']
        action_enable = {
            "jsonrpc": "2.0",
            "method": "action.update",
            "params": {"actionid": action_id, "status": 0}, # 0 is enabled
            "id": 4,
            "auth": auth_token
        }
        res_act = requests.post(ZABBIX_API_URL, json=action_enable).json()
        if 'result' in res_act:
            print(f"Alert Action '{actions[0]['name']}' successfully enabled.")
        else:
            print(f"Failed to enable action: {res_act}")
    else:
        print("Could not find default action 'Report problems to Zabbix administrators' to enable.")

if __name__ == "__main__":
    email = get_email_from_env()
    token = authenticate()
    if token:
        configure_email(token, email)
    else:
        print("Could not authenticate to Zabbix on localhost:8081.")

import requests
import json
import time

ZABBIX_API_URL = "http://localhost:8080/api_jsonrpc.php"
ZABBIX_USER = "Admin"
ZABBIX_PASSWORD = "zabbix" # Default zabbix admin password

def authenticate():
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": ZABBIX_USER,
            "password": ZABBIX_PASSWORD
        },
        "id": 1,
        "auth": None
    }
    response = requests.post(ZABBIX_API_URL, json=payload).json()
    if 'result' in response:
        return response['result']
    else:
        print(f"Authentication failed: {response}")
        return None

def get_triggers(auth_token, description_search):
    payload = {
        "jsonrpc": "2.0",
        "method": "trigger.get",
        "params": {
            "output": ["triggerid", "description"],
            "search": {
                "description": description_search
            }
        },
        "id": 2,
        "auth": auth_token
    }
    response = requests.post(ZABBIX_API_URL, json=payload).json()
    return response.get('result', [])

def set_dependency(auth_token, trigger_id, depends_on_trigger_id):
    payload = {
        "jsonrpc": "2.0",
        "method": "trigger.update",
        "params": {
            "triggerid": trigger_id,
            "dependencies": [
                {"triggerid": depends_on_trigger_id}
            ]
        },
        "id": 3,
        "auth": auth_token
    }
    response = requests.post(ZABBIX_API_URL, json=payload).json()
    if 'result' in response:
        print(f"Successfully added dependency! Trigger {trigger_id} now depends on {depends_on_trigger_id}")
    else:
        print(f"Failed to add dependency: {response}")

if __name__ == "__main__":
    print("Waiting for Zabbix server to start...")
    time.sleep(10) # Simple wait
    
    try:
        auth_token = authenticate()
        if not auth_token:
            print("Cannot proceed without authentication.")
            exit(1)
            
        # Example logic to find DB and App triggers (Names will depend on actual Zabbix config)
        db_triggers = get_triggers(auth_token, "MySQL is down")
        app_triggers = get_triggers(auth_token, "Application Food AI Down")
        
        if not db_triggers or not app_triggers:
            print("Could not find the necessary triggers. They might need to be created first in Zabbix.")
            print(f"DB Triggers found: {db_triggers}")
            print(f"App Triggers found: {app_triggers}")
        else:
            db_trigger_id = db_triggers[0]['triggerid']
            app_trigger_id = app_triggers[0]['triggerid']
            set_dependency(auth_token, app_trigger_id, db_trigger_id)
            
    except Exception as e:
        print(f"Error configuring Zabbix: {e}")

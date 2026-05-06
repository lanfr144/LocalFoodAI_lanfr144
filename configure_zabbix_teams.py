import requests
import json
import os

ZABBIX_API_URL = "http://zabbix-web:8080/api_jsonrpc.php"
ZABBIX_USER = "Admin"
ZABBIX_PASSWORD = "zabbix"
TEAMS_WEBHOOK_URL = "https://webhookbot.c-toss.com/api/bot/webhooks/7accc381-ae55-423c-9c08-6764c2813c8a"

def authenticate():
    payload = {"jsonrpc": "2.0", "method": "user.login", "params": {"username": ZABBIX_USER, "password": ZABBIX_PASSWORD}, "id": 1}
    try:
        response = requests.post(ZABBIX_API_URL, json=payload).json()
        return response.get('result')
    except Exception as e:
        print(f"Error connecting to Zabbix API: {e}")
        return None

def configure_teams(auth_token):
    print("Checking if MS Teams Webhook Media Type already exists...")
    check_payload = {
        "jsonrpc": "2.0",
        "method": "mediatype.get",
        "params": {
            "output": ["mediatypeid", "name"],
            "search": {"name": "MS Teams Custom Webhook"}
        },
        "id": 2,
        "auth": auth_token
    }
    existing = requests.post(ZABBIX_API_URL, json=check_payload).json().get('result', [])
    
    if existing:
        media_type_id = existing[0]['mediatypeid']
        print(f"Media Type already exists with ID {media_type_id}. Updating it...")
        update_payload = {
            "jsonrpc": "2.0",
            "method": "mediatype.update",
            "params": {
                "mediatypeid": media_type_id,
                "parameters": [
                    { "name": "URL", "value": TEAMS_WEBHOOK_URL },
                    { "name": "Message", "value": "{ALERT.SUBJECT}\\n{ALERT.MESSAGE}" }
                ]
            },
            "id": 3,
            "auth": auth_token
        }
        requests.post(ZABBIX_API_URL, json=update_payload)
    else:
        print("Creating MS Teams Webhook Media Type...")
        create_payload = {
            "jsonrpc": "2.0",
            "method": "mediatype.create",
            "params": {
                "type": 4, # 4 = Webhook
                "name": "MS Teams Custom Webhook",
                "script": "var req = new HttpRequest(); req.addHeader('Content-Type: application/json'); var params = JSON.parse(value); var payload = {'text': params.Message}; var resp = req.post(params.URL, JSON.stringify(payload)); Zabbix.log(4, '[Teams Webhook] response: ' + resp); return 'OK';",
                "parameters": [
                    { "name": "URL", "value": TEAMS_WEBHOOK_URL },
                    { "name": "Message", "value": "{ALERT.SUBJECT}\\n{ALERT.MESSAGE}" }
                ]
            },
            "id": 4,
            "auth": auth_token
        }
        res = requests.post(ZABBIX_API_URL, json=create_payload).json()
        if 'result' in res:
            media_type_id = res['result']['mediatypeids'][0]
            print(f"Created Media Type with ID: {media_type_id}")
        else:
            print(f"Failed to create Media Type: {res}")
            return

    # Assign to Admin user
    print("Assigning Teams Webhook to Admin User...")
    user_payload = {
        "jsonrpc": "2.0",
        "method": "user.update",
        "params": {
            "userid": "1",
            "medias": [
                {
                    "mediatypeid": "1", # Email
                    "sendto": ["lanfr144@gmail.com"],
                    "active": 0,
                    "severity": 63,
                    "period": "1-7,00:00-24:00"
                },
                {
                    "mediatypeid": media_type_id, # Teams
                    "sendto": ["teams"],
                    "active": 0,
                    "severity": 63,
                    "period": "1-7,00:00-24:00"
                }
            ]
        },
        "id": 5,
        "auth": auth_token
    }
    res = requests.post(ZABBIX_API_URL, json=user_payload).json()
    if 'result' in res:
        print("User media successfully updated to include Teams.")
    else:
        print(f"Failed to update user media: {res}")

    # Ensure action is enabled
    print("Enabling Report problems to Zabbix administrators action...")
    action_search = {
        "jsonrpc": "2.0",
        "method": "action.get",
        "params": {
            "output": ["actionid", "name"],
            "search": {"name": "Report problems to Zabbix administrators"}
        },
        "id": 6,
        "auth": auth_token
    }
    actions = requests.post(ZABBIX_API_URL, json=action_search).json().get('result', [])
    if actions:
        action_id = actions[0]['actionid']
        action_enable = {
            "jsonrpc": "2.0",
            "method": "action.update",
            "params": {"actionid": action_id, "status": 0},
            "id": 7,
            "auth": auth_token
        }
        requests.post(ZABBIX_API_URL, json=action_enable)
        print("Action verified and enabled.")
        
        # Send a test message
        test_payload = {
            "text": "Hello World, From Zabbix Automated Webhook Script!"
        }
        print("Sending test message to Teams...")
        try:
            requests.post(TEAMS_WEBHOOK_URL, json=test_payload)
            print("Test message sent!")
        except Exception as e:
            print(f"Failed to send test message: {e}")

if __name__ == "__main__":
    token = authenticate()
    if token:
        configure_teams(token)
    else:
        print("Failed to authenticate to Zabbix API.")

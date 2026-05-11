import requests

ZABBIX_API_URL = "http://192.168.130.170:8081/api_jsonrpc.php"
ZABBIX_USER = "Admin"
ZABBIX_PASSWORD = "zabbix"

def authenticate():
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {"username": ZABBIX_USER, "password": ZABBIX_PASSWORD},
        "id": 1
    }
    try:
        response = requests.post(ZABBIX_API_URL, json=payload).json()
        return response.get('result')
    except Exception as e:
        print(f"Error connecting to Zabbix API: {e}")
        return None

def get_snmp_item_id(auth_token):
    # Retrieve the SNMP fallback item which catches all traps
    payload = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": ["itemid", "name", "key_"],
            "search": {
                "key_": "snmptrap.fallback"
            }
        },
        "id": 2,
        "auth": auth_token
    }
    response = requests.post(ZABBIX_API_URL, json=payload).json()
    items = response.get('result', [])
    if items:
        print(f"Found SNMP Trap Item: {items[0]['itemid']}")
        return items[0]['itemid']
    else:
        # Fallback to search any SNMP trap item
        payload["params"]["search"] = {"key_": "snmptrap["}
        response = requests.post(ZABBIX_API_URL, json=payload).json()
        items = response.get('result', [])
        if items:
            print(f"Found specific SNMP Trap Item: {items[0]['itemid']}")
            return items[0]['itemid']
    print("Could not find any SNMP Trap item in Zabbix.")
    return None

def create_dashboard(auth_token, item_id):
    print("Creating Food AI RAG Telemetry Dashboard...")
    
    # A Plaintext widget needs the itemid passed correctly in fields
    widget_fields = []
    if item_id:
        widget_fields = [
            {"type": 4, "name": "itemids", "value": item_id},
            {"type": 0, "name": "show_lines", "value": 25}
        ]

    payload = {
        "jsonrpc": "2.0",
        "method": "dashboard.create",
        "params": {
            "name": "Food AI RAG Telemetry (Live)",
            "userid": "1",
            "pages": [
                {
                    "name": "SNMP Trap Activity",
                    "widgets": [
                        {
                            "type": "plaintext",
                            "name": "Ingestion Row Count Log",
                            "x": 0, "y": 0, "width": 12, "height": 8,
                            "fields": widget_fields
                        },
                        {
                            "type": "systeminfo",
                            "name": "Server Status",
                            "x": 12, "y": 0, "width": 12, "height": 8
                        }
                    ]
                }
            ]
        },
        "id": 3,
        "auth": auth_token
    }
    response = requests.post(ZABBIX_API_URL, json=payload).json()
    if 'result' in response:
        print(f"Dashboard Created successfully! ID: {response['result']['dashboardids'][0]}")
    else:
        print(f"Failed to create dashboard: {response}")

if __name__ == "__main__":
    token = authenticate()
    if token:
        item_id = get_snmp_item_id(token)
        create_dashboard(token, item_id)
    else:
        print("❌ Could not authenticate to Zabbix. Ensure the server is fully started on port 8081.")

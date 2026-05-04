import requests

ZABBIX_API_URL = "http://localhost:8081/api_jsonrpc.php"
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

def create_dashboard(auth_token):
    print("Creating Food AI RAG Telemetry Dashboard...")
    payload = {
        "jsonrpc": "2.0",
        "method": "dashboard.create",
        "params": {
            "name": "Food AI RAG Telemetry",
            "userid": "1",
            "pages": [
                {
                    "name": "SNMP Trap Activity",
                    "widgets": [
                        {
                            "type": "svggraph",
                            "name": "Ingestion Activity",
                            "x": 0, "y": 0, "width": 12, "height": 5,
                            "fields": [
                                {"type": 1, "name": "ds.0.color", "value": "FF0000"}
                            ]
                        },
                        {
                            "type": "systeminfo",
                            "name": "Server Status",
                            "x": 12, "y": 0, "width": 12, "height": 5
                        }
                    ]
                }
            ]
        },
        "id": 2,
        "auth": auth_token
    }
    response = requests.post(ZABBIX_API_URL, json=payload).json()
    if 'result' in response:
        print(f"✅ Dashboard Created successfully! ID: {response['result']['dashboardids'][0]}")
    else:
        print(f"⚠️ Failed to create dashboard: {response}")

if __name__ == "__main__":
    token = authenticate()
    if token:
        create_dashboard(token)
    else:
        print("❌ Could not authenticate to Zabbix. Ensure the server is fully started on port 8081.")

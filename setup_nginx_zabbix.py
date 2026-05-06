import requests
import json
import os

ZABBIX_API_URL = "http://zabbix-web:8080/api_jsonrpc.php"
ZABBIX_USER = "Admin"
ZABBIX_PASSWORD = "zabbix"

def authenticate():
    payload = {"jsonrpc": "2.0", "method": "user.login", "params": {"username": ZABBIX_USER, "password": ZABBIX_PASSWORD}, "id": 1}
    try:
        response = requests.post(ZABBIX_API_URL, json=payload).json()
        return response.get('result')
    except Exception as e:
        print(f"Error connecting to Zabbix API: {e}")
        return None

def configure_nginx_web_scenario(auth_token):
    # Get Zabbix server host ID
    host_search = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "filter": {"host": ["Zabbix server"]}
        },
        "id": 2,
        "auth": auth_token
    }
    hosts = requests.post(ZABBIX_API_URL, json=host_search).json().get('result', [])
    if not hosts:
        print("Could not find Zabbix server host.")
        return
    host_id = hosts[0]['hostid']

    print("Checking if Nginx Web Scenario already exists...")
    scenario_search = {
        "jsonrpc": "2.0",
        "method": "httptest.get",
        "params": {
            "filter": {"name": ["Nginx Streamlit Proxy Check"]}
        },
        "id": 3,
        "auth": auth_token
    }
    scenarios = requests.post(ZABBIX_API_URL, json=scenario_search).json().get('result', [])
    
    if scenarios:
        print("Nginx Web Scenario already exists.")
        return

    print("Creating Nginx Web Scenario...")
    create_payload = {
        "jsonrpc": "2.0",
        "method": "httptest.create",
        "params": {
            "name": "Nginx Streamlit Proxy Check",
            "hostid": host_id,
            "delay": "1m",
            "retries": 3,
            "steps": [
                {
                    "name": "Check Proxy Root",
                    "url": "http://nginx:80",
                    "status_codes": "200",
                    "no": 1
                }
            ]
        },
        "id": 4,
        "auth": auth_token
    }
    res = requests.post(ZABBIX_API_URL, json=create_payload).json()
    if 'result' in res:
        print(f"Successfully created Nginx Web Scenario.")
    else:
        print(f"Failed to create Web Scenario: {res}")

if __name__ == "__main__":
    token = authenticate()
    if token:
        configure_nginx_web_scenario(token)
    else:
        print("Failed to authenticate to Zabbix API.")

import requests
import json
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()
urllib3.disable_warnings()

# Zabbix Server credentials loaded from environment
ZABBIX_URL = os.environ.get('ZABBIX_URL', '')
ZABBIX_USER = os.environ.get('ZABBIX_USER', '')
ZABBIX_PASS = os.environ.get('ZABBIX_PASS', '')

def zabbix_rpc(method, params, auth=None):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    if auth:
        payload["auth"] = auth
    
    response = requests.post(ZABBIX_URL, json=payload, headers={'Content-Type': 'application/json-rpc'})
    return response.json()

def main():
    print("Authenticating with Zabbix...")
    res = zabbix_rpc('user.login', {'username': ZABBIX_USER, 'password': ZABBIX_PASS})
    if 'error' in res:
        print("Login failed:", res['error'])
        return
        
    auth_token = res['result']
    
    print("Finding Zabbix server host...")
    hosts = zabbix_rpc('host.get', {
        'filter': {'host': ['Zabbix server']}
    }, auth=auth_token)
    
    if not hosts['result']:
        print("Error: Could not find 'Zabbix server' host in Zabbix.")
        return
        
    host_id = hosts['result'][0]['hostid']
    
    print("Checking if Airflow Web Scenario already exists...")
    scenarios = zabbix_rpc('httptest.get', {
        'hostids': host_id,
        'filter': {'name': ['Airflow Supervisor Health']}
    }, auth=auth_token)
    
    if scenarios['result']:
        print("Airflow Web Scenario already exists. Deleting to recreate...")
        httptest_id = scenarios['result'][0]['httptestid']
        zabbix_rpc('httptest.delete', [httptest_id], auth=auth_token)
        
    print("Creating Airflow Web Scenario...")
    create_res = zabbix_rpc('httptest.create', {
        "name": "Airflow Supervisor Health",
        "hostid": host_id,
        "delay": "1m",
        "steps": [
            {
                "name": "Check Airflow Health Endpoint",
                "url": "http://172.18.0.1:8082/health",
                "status_codes": "200",
                "no": 1
            }
        ]
    }, auth=auth_token)
    
    if 'error' in create_res:
        print("Error creating web scenario:", create_res['error'])
    else:
        print("Successfully created Zabbix monitoring for Apache Airflow!")

if __name__ == "__main__":
    main()

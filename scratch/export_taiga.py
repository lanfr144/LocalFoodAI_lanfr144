import requests
import urllib3
import os
import json
import time

urllib3.disable_warnings()

TAIGA_USER = os.environ.get('TAIGA_USER', 'FrancoisLange')
TAIGA_PASS = os.environ.get('TAIGA_PASS', 'your_db_password_here')
base_url = 'https://192.168.130.161/taiga/api/v1'

def main():
    auth_resp = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': TAIGA_USER, 'password': TAIGA_PASS}, verify=False)
    if auth_resp.status_code != 200:
        print("Auth failed!")
        return
        
    auth = auth_resp.json()
    headers = {
        'Authorization': f'Bearer {auth["auth_token"]}', 
        'Content-Type': 'application/json'
    }
    project_id = 21
    
    # In Taiga, request a dump
    print("Requesting Taiga project export...")
    resp = requests.post(f'{base_url}/exporter/{project_id}/dump', headers=headers, verify=False)
    if resp.status_code == 202:
        print("Export is being processed...")
        # Poll for the export dump file
        for _ in range(30):
            time.sleep(2)
            export_status = requests.get(f'{base_url}/exporter/{project_id}', headers=headers, verify=False).json()
            if 'export_file' in export_status and export_status['export_file']:
                file_url = export_status['export_file']
                print(f"Export file is ready: {file_url}")
                # Download it
                file_resp = requests.get(file_url, headers=headers, verify=False)
                with open(r'c:\Users\lanfr144\Documents\DOPRO1\Antigravity\taiga_export.json', 'wb') as f:
                    f.write(file_resp.content)
                print("Export successfully saved to Antigravity/taiga_export.json")
                return
    else:
        print(f"Direct export request failed: {resp.status_code} - {resp.text}")
        
        # Let's try to query the export configuration to see if there is already an existing dump
        export_status = requests.get(f'{base_url}/exporter/{project_id}', headers=headers, verify=False).json()
        print("Existing export details:", export_status)
        if 'export_file' in export_status and export_status['export_file']:
            file_url = export_status['export_file']
            print(f"Downloading existing export: {file_url}")
            file_resp = requests.get(file_url, headers=headers, verify=False)
            with open(r'c:\Users\lanfr144\Documents\DOPRO1\Antigravity\taiga_export.json', 'wb') as f:
                f.write(file_resp.content)
            print("Export successfully saved to Antigravity/taiga_export.json")
            return
            
if __name__ == '__main__':
    main()

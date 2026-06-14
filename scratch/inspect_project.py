import requests
import urllib3
import os
import json

urllib3.disable_warnings()

auth = requests.post('https://192.168.130.161/taiga/api/v1/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'your_db_password_here'}, verify=False).json()
h = {'Authorization': f'Bearer {auth["auth_token"]}'}
p = requests.get('https://192.168.130.161/taiga/api/v1/projects/21', headers=h, verify=False).json()

# Write project dictionary to a temporary text file so we can view it
with open('scratch/project_details.json', 'w') as f:
    json.dump(p, f, indent=2)
print("Project details saved to scratch/project_details.json")

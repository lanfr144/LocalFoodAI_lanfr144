import requests
import urllib3
urllib3.disable_warnings()

auth = requests.post(
    'https://192.168.130.161/taiga/api/v1/auth', 
    json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, 
    verify=False
).json()

headers = {'Authorization': f'Bearer {auth["auth_token"]}'}
projs = requests.get('https://192.168.130.161/taiga/api/v1/projects', headers=headers, verify=False).json()
print("Projects:")
for p in projs:
    print(f"ID: {p['id']}, Name: {p['name']}, Slug: {p['slug']}")

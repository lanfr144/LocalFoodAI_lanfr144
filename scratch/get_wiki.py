import requests
import urllib3

urllib3.disable_warnings()

base_url = 'https://192.168.130.161/taiga/api/v1'
auth_resp = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'your_db_password_here'}, verify=False)
if auth_resp.status_code == 200:
    auth = auth_resp.json()
    h = {'Authorization': f'Bearer {auth["auth_token"]}'}
    res = requests.get(f'{base_url}/wiki?project=21', headers=h, verify=False).json()
    for w in res:
        print(f"Slug: {w['slug']}, Title: {w.get('subject') or w['slug']}")
else:
    print("Auth failed", auth_resp.status_code, auth_resp.text)

import requests, urllib3
urllib3.disable_warnings()
auth = requests.post('https://192.168.130.161/taiga/api/v1/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}'}

epic_statuses = requests.get('https://192.168.130.161/taiga/api/v1/epic-statuses?project=21', headers=headers, verify=False).json()
epic_closed_status = next((s['id'] for s in epic_statuses if s['is_closed']), None)

epic = requests.get('https://192.168.130.161/taiga/api/v1/epics/by_ref?ref=28&project=21', headers=headers, verify=False).json()
if 'id' in epic:
    resp = requests.patch(f'https://192.168.130.161/taiga/api/v1/epics/{epic["id"]}', headers=headers, json={'status': epic_closed_status, 'version': epic['version']}, verify=False)
    print(f'Epic TG-{epic["ref"]} Closing Status: {resp.status_code}')

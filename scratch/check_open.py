import requests
import urllib3
urllib3.disable_warnings()
base_url='https://192.168.130.161/taiga/api/v1'
auth=requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'your_db_password_here'}, verify=False).json()
h={'Authorization': f'Bearer {auth["auth_token"]}', 'x-disable-pagination': 'true'}
ts=requests.get(f'{base_url}/tasks?project=21', headers=h, verify=False).json()
open_tasks = [{'id': t['id'], 'ref': t['ref'], 'subject': t['subject'], 'status': t['status'], 'us': t.get('user_story')} for t in ts if t['status'] != 104]
print("Open Tasks:", open_tasks)
us=requests.get(f'{base_url}/userstories?project=21', headers=h, verify=False).json()
open_us = [{'id': u['id'], 'ref': u['ref'], 'subject': u['subject'], 'status': u['status']} for u in us if u['status'] != 125]
print("Open US:", open_us)

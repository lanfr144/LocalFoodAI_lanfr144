import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth = requests.post(
    'https://192.168.130.161/taiga/api/v1/auth', 
    json={'type': 'normal', 'username': 'lanfr1904@outlook.com', 'password': 'BTSai123'}, 
    verify=False
).json()

headers = {'Authorization': f'Bearer {auth["auth_token"]}'}
proj_id = 21

m_res = requests.get(f'https://192.168.130.161/taiga/api/v1/milestones?project={proj_id}', headers=headers, verify=False).json()
print('Milestones:', [(m['name'], m['id']) for m in m_res])

w_res = requests.get(f'https://192.168.130.161/taiga/api/v1/wiki?project={proj_id}', headers=headers, verify=False)
if w_res.status_code == 200:
    print('Wikis:', [(w['slug'], w['id']) for w in w_res.json()])
else:
    print('Wiki error:', w_res.text)

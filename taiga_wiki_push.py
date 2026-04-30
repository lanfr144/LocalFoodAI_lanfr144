import requests
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = 'https://192.168.130.161/taiga/api/v1'
auth_url = f'{base_url}/auth'
auth = requests.post(auth_url, json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

def push_wiki(slug, md_path):
    with open(md_path, 'r') as f:
        content = f.read()
    
    res = requests.get(f'{base_url}/wiki?project={proj_id}&slug={slug}', headers=headers, verify=False).json()
    if len(res) > 0:
        wiki_id = res[0]['id']
        version = res[0]['version']
        payload = {'content': content, 'version': version}
        r = requests.put(f'{base_url}/wiki/{wiki_id}', json=payload, headers=headers, verify=False)
        print(f'Updated {slug}: {r.status_code}')
    else:
        payload = {'project': proj_id, 'slug': slug, 'content': content}
        r = requests.post(f'{base_url}/wiki', json=payload, headers=headers, verify=False)
        print(f'Created {slug}: {r.status_code}')

# In Taiga, the home page of the wiki is usually 'home'
push_wiki('home', 'docs/Scrum_Wiki.md')
push_wiki('backup-procedure', 'docs/Backup_Procedure.md')
push_wiki('wsl-deployment', 'docs/WSL_Deployment.md')
push_wiki('test-cases-sprint8', 'docs/Test_Cases_Sprint8.md')

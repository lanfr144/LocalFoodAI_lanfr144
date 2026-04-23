import requests, urllib3
urllib3.disable_warnings()

auth = requests.post(
    'https://192.168.130.161/taiga/api/v1/auth', 
    json={'type': 'normal', 'username': 'lanfr1904@outlook.com', 'password': 'BTSai123'}, 
    verify=False
).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}'}

proj_id = 21

pts = requests.get(f'https://192.168.130.161/taiga/api/v1/points?project={proj_id}', headers=headers, verify=False).json()
pt_map = {p['value']: p['id'] for p in pts}
five_pt_id = pt_map.get(5)
roles = requests.get(f'https://192.168.130.161/taiga/api/v1/roles?project={proj_id}', headers=headers, verify=False).json()
role_id = roles[0]['id']

us_list = requests.get(f'https://192.168.130.161/taiga/api/v1/userstories?project={proj_id}', headers=headers, verify=False).json()
for us in us_list:
    if us.get('total_points') == 0 or us.get('total_points') is None:
        points_payload = us.get('points', {})
        points_payload[str(role_id)] = five_pt_id
        
        resp = requests.patch(
            f'https://192.168.130.161/taiga/api/v1/userstories/{us["id"]}', 
            headers=headers, 
            json={'points': points_payload, 'version': us['version']}, 
            verify=False
        )
        print(f"Patched US {us['ref']} to 5 Points! Status: {resp.status_code}")

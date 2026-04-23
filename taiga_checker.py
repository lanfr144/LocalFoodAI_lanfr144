import requests, urllib3
urllib3.disable_warnings()

auth = requests.post(
    'https://192.168.130.161/taiga/api/v1/auth', 
    json={'type': 'normal', 'username': 'lanfr1904@outlook.com', 'password': 'BTSai123'}, 
    verify=False
).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}'}

proj_id = 21

print("=== User Stories missing Tasks ===")
us_list = requests.get(f'https://192.168.130.161/taiga/api/v1/userstories?project={proj_id}', headers=headers, verify=False).json()
for us in us_list:
    tasks = requests.get(f'https://192.168.130.161/taiga/api/v1/tasks?user_story={us["id"]}', headers=headers, verify=False).json()
    if len(tasks) == 0:
        print(f"US #{us['ref']}: {us['subject']}")

print("\n=== User Stories missing Points ===")
for us in us_list:
    if us.get('total_points') == 0 or us.get('total_points') is None:
        print(f"US #{us['ref']}: {us['subject']} (Points: {us.get('total_points')})")


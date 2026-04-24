import requests, urllib3
urllib3.disable_warnings()

auth = requests.post(
    'https://192.168.130.161/taiga/api/v1/auth', 
    json={'type': 'normal', 'username': 'lanfr1904@outlook.com', 'password': 'BTSai123'}, 
    verify=False
).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}'}
proj_id = 21
sprint4_id = 71

us_list = requests.get(f'https://192.168.130.161/taiga/api/v1/userstories?project={proj_id}', headers=headers, verify=False).json()

tasks = [
    "Refactor Cryptography Bug - Replace dynamic salting loop with bcrypt.checkpw",
    "Implement Horizontal Table Partitioning to bypass MySQL 65KB InnoDB limit",
    "Construct dynamic UI multiselect for mapping 200 CSV columns seamlessly",
    "Bind Pandas dataframes tightly to Memory logic preventing UI crashes",
    "Overwrite LLM system prompts strictly for native Markdown gram output",
    "Configure native mail throttle limits to block .pt.lu bounce delays"
]

target_us = None
for us in us_list:
    if "Sprint 4" in us['subject'] or us['milestone'] is None:
        target_us = us
        # Patch US to Sprint 4 milestone
        res = requests.patch(f"https://192.168.130.161/taiga/api/v1/userstories/{us['id']}", 
            headers=headers, 
            json={"milestone": sprint4_id, "version": us['version']}, 
            verify=False)
        print(f"Mapped US {us['id']} ({us['subject']}) into Sprint 4 Milestone!")
        
        for t in tasks:
            requests.post('https://192.168.130.161/taiga/api/v1/tasks', headers=headers, json={"project": proj_id, "user_story": us['id'], "subject": t}, verify=False)
        print(f"Successfully appended granular deployment tasks into US: {us['id']}")
        
if not target_us:
    print("No open unassigned User Stories found to append Sprint 4 data.")

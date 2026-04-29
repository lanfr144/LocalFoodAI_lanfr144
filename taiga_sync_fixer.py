import requests, urllib3
urllib3.disable_warnings()

# Configuration – adjust as needed
TAIGA_URL = 'https://192.168.130.161/taiga/api/v1'
USERNAME = 'lanfr1904@outlook.com'
PASSWORD = 'BTSai123'
PROJECT_ID = 21
DEFAULT_TASK_SUBJECT = 'Auto‑generated task (define details)'
DEFAULT_POINTS = 1

# Authenticate and obtain token
auth_resp = requests.post(
    f'{TAIGA_URL}/auth',
    json={'type': 'normal', 'username': USERNAME, 'password': PASSWORD},
    verify=False
).json()

token = auth_resp.get('auth_token')
if not token:
    raise RuntimeError('Authentication to Taiga failed')
headers = {'Authorization': f'Bearer {token}'}

# Helper functions
def get_user_stories():
    resp = requests.get(
        f'{TAIGA_URL}/userstories?project={PROJECT_ID}',
        headers=headers,
        verify=False
    )
    resp.raise_for_status()
    return resp.json()

def get_tasks_for_us(us_id):
    resp = requests.get(
        f'{TAIGA_URL}/tasks?user_story={us_id}',
        headers=headers,
        verify=False
    )
    resp.raise_for_status()
    return resp.json()

def create_task(us_id):
    payload = {
        'subject': DEFAULT_TASK_SUBJECT,
        'user_story': us_id,
        'project': PROJECT_ID,
        'status': 101  # Status 101 = "New" for project 21
    }
    resp = requests.post(
        f'{TAIGA_URL}/tasks',
        json=payload,
        headers=headers,
        verify=False
    )
    if not resp.ok:
        print("Error creating task:", resp.text)
    resp.raise_for_status()
    return resp.json()

def set_points(us_id, points, version):
    payload = {
        'total_points': points,
        'version': version
    }
    resp = requests.patch(
        f'{TAIGA_URL}/userstories/{us_id}',
        json=payload,
        headers=headers,
        verify=False
    )
    if not resp.ok:
        print("Error setting points:", resp.text)
    resp.raise_for_status()
    return resp.json()

def main():
    us_list = get_user_stories()
    for us in us_list:
        # 1️⃣ Ensure at least one task exists
        tasks = get_tasks_for_us(us['id'])
        if not tasks:
            print(f"US #{us['ref']} missing tasks – creating default task")
            create_task(us['id'])
        # 2️⃣ Ensure story has points
        if not us.get('total_points'):
            print(f"US #{us['ref']} missing points – setting to {DEFAULT_POINTS}")
            set_points(us['id'], DEFAULT_POINTS, us['version'])

if __name__ == '__main__':
    main()

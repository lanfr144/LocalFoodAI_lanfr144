import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = 'https://192.168.130.161/taiga/api/v1'
auth_url = f'{base_url}/auth'
auth = requests.post(auth_url, json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

# Fetch all existing links
existing = requests.get(f'{base_url}/wiki-links?project={proj_id}', headers=headers, verify=False).json()

# Delete the ones I made previously that had parentheses
for link in existing:
    if "26.04.30" in link['title']:
        requests.delete(f'{base_url}/wiki-links/{link["id"]}', headers=headers, verify=False)
        print(f"Deleted old link: {link['title']}")

bookmarks = [
    {"title": "26.04.30 PLAN", "href": "26-04-30-plan"},
    {"title": "26.04.30 DAILY", "href": "26-04-30-daily"},
    {"title": "26.04.30 REVIEW", "href": "26-04-30-review"},
    {"title": "26.04.30 RETROSPECTIVE", "href": "26-04-30-retrospective"},
    {"title": "26.04.30 ARTIFACT", "href": "26-04-30-artifact"}
]

# Calculate fresh order
existing = requests.get(f'{base_url}/wiki-links?project={proj_id}', headers=headers, verify=False).json()
max_order = max([e['order'] for e in existing]) if existing else 0

for i, b in enumerate(bookmarks):
    payload = {
        "project": proj_id,
        "title": b["title"],
        "href": b["href"],
        "order": max_order + i + 1
    }
    r = requests.post(f'{base_url}/wiki-links', json=payload, headers=headers, verify=False)
    print(f'Created Bookmark {b["title"]}: {r.status_code}')

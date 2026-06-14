import requests
import urllib3
urllib3.disable_warnings()

base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'your_db_password_here'}, verify=False).json()
if 'auth_token' not in auth:
    print("Authentication failed:", auth)
    exit(1)

h = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
project_id = 21

pages = [
    {"slug": "26-05-15-retrospective", "content": "# 26.05.15 RETROSPECTIVE\n\nReview for the two last weeks."},
    {"slug": "26-05-15-plan", "content": "# 26.05.15 PLAN\n\nCreate a plan for this week."},
    {"slug": "26-05-15-review", "content": "# 26.05.15 REVIEW\n\nCreate a review the two last weeks."},
    {"slug": "26-05-15-daily", "content": "# 26.05.15 DAILY\n\nDaily for today."}
]

for page in pages:
    payload = {
        "project": project_id,
        "slug": page["slug"],
        "content": page["content"]
    }
    r = requests.post(f'{base_url}/wiki', json=payload, headers=h, verify=False)
    if r.status_code == 201:
        print(f"Created: {page['slug']}")
    elif r.status_code == 400 and "already exists" in r.text.lower():
        print(f"Already exists: {page['slug']}")
    else:
        print(f"Failed to create {page['slug']}: {r.status_code} {r.text}")

# We also need to add them to the wiki links (bookmarks in Taiga)
# The user said: "create the bookmarks in wiki for today with the following entries"
# Bookmarks are usually created via POST /api/v1/wiki-links
links = [
    {"title": "26.05.15 RETROSPECTIVE", "href": "26-05-15-retrospective"},
    {"title": "26.05.15 PLAN", "href": "26-05-15-plan"},
    {"title": "26.05.15 REVIEW", "href": "26-05-15-review"},
    {"title": "26.05.15 DAILY", "href": "26-05-15-daily"}
]

for link in links:
    payload = {
        "project": project_id,
        "title": link["title"],
        "href": link["href"]
    }
    r = requests.post(f'{base_url}/wiki-links', json=payload, headers=h, verify=False)
    if r.status_code == 201:
        print(f"Created link: {link['title']}")
    else:
        print(f"Failed to create link {link['title']}: {r.status_code} {r.text}")

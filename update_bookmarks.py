import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
base_url = 'https://192.168.130.161/taiga/api/v1'
auth = requests.post(f'{base_url}/auth', json={'type': 'normal', 'username': 'FrancoisLange', 'password': 'BTSai123'}, verify=False).json()
headers = {'Authorization': f'Bearer {auth["auth_token"]}', 'Content-Type': 'application/json'}
proj_id = 21

slug = 'home'
check_req = requests.get(f'{base_url}/wiki?project={proj_id}&slug={slug}', headers=headers, verify=False)
if check_req.status_code == 200:
    wiki_pages = check_req.json()
    if len(wiki_pages) > 0:
        page_id = wiki_pages[0]['id']
        version = wiki_pages[0]['version']
        content = wiki_pages[0]['content']
        
        # Append the new links if they aren't there
        new_links = """
- [26.05.07 DAILY](260507-daily)
- [26.05.07 REVIEW](260507-review)
- [26.05.07 RETROSPECTIVE](260507-retrospective)
- [26.05.07 PLAN](260507-plan)
"""
        if "260507-daily" not in content:
            content += new_links
            payload = {
                "project": proj_id,
                "slug": slug,
                "content": content,
                "version": version
            }
            res = requests.put(f'{base_url}/wiki/{page_id}', json=payload, headers=headers, verify=False)
            if res.status_code == 200:
                print("Bookmarks updated successfully!")
            else:
                print(f"Failed to update bookmarks: {res.text}")
        else:
            print("Bookmarks already up to date.")

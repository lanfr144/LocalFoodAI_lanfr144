import json
import urllib.request

ZABBIX_URL = 'http://192.168.130.170:8081/api_jsonrpc.php'
ZABBIX_USER = 'Admin'
ZABBIX_PASS = 'zabbix'
DISCORD_WEBHOOK = 'https://discord.com/api/webhooks/1504740323576774739/2-MNclIGcYSxtLrQ-jzIXWl6miW3dOFTvB6KZsTQIX1FFis6JFoszATegAJoosJD7CMT'
EMAIL_USER = 'lanfr144@gmail.com'
EMAIL_PASS = '321iaSTB'

def zabbix_request(method, params, auth=None):
    payload = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': 1
    }
    if auth:
        payload['auth'] = auth
        
    req = urllib.request.Request(ZABBIX_URL, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json-rpc'})
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        if 'error' in res:
            print(f"Error in {method}: {res['error']}")
            return None
        return res['result']

def main():
    # 1. Login
    auth_token = zabbix_request('user.login', {'username': ZABBIX_USER, 'password': ZABBIX_PASS})
    if not auth_token:
        print("Login failed")
        return
    print("Zabbix Auth Token:", auth_token)

    # 2. Configure Email Media Type
    # Find existing Email media type (type 0 = Email)
    email_mt = zabbix_request('mediatype.get', {'filter': {'type': '0'}}, auth_token)
    email_params = {
        'type': '0',
        'name': 'Email',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': '587',
        'smtp_helo': 'gmail.com',
        'smtp_email': EMAIL_USER,
        'smtp_security': '1', # STARTTLS
        'smtp_verify_peer': '0',
        'smtp_verify_host': '0',
        'smtp_authentication': '1',
        'username': EMAIL_USER,
        'passwd': EMAIL_PASS,
        'content_type': '1' # HTML
    }
    
    if email_mt:
        email_params['mediatypeid'] = email_mt[0]['mediatypeid']
        zabbix_request('mediatype.update', email_params, auth_token)
        print("Updated Email Media Type")
        email_id = email_mt[0]['mediatypeid']
    else:
        res = zabbix_request('mediatype.create', email_params, auth_token)
        email_id = res['mediatypeids'][0]
        print("Created Email Media Type")

    # 3. Configure Discord Media Type (type 4 = Webhook)
    discord_script = """
    var req = new HttpRequest();
    req.addHeader('Content-Type: application/json');
    var webhook = params.URL;
    var payload = JSON.stringify({
        "content": params.Subject + "\\n" + params.Message
    });
    var resp = req.post(webhook, payload);
    if (req.getStatus() != 204 && req.getStatus() != 200) {
        throw 'Failed with status ' + req.getStatus();
    }
    return 'OK';
    """
    
    discord_mt = zabbix_request('mediatype.get', {'filter': {'name': 'Discord Webhook'}}, auth_token)
    discord_params = {
        'name': 'Discord Webhook',
        'type': '4',
        'parameters': [
            {'name': 'URL', 'value': DISCORD_WEBHOOK},
            {'name': 'Subject', 'value': '{ALERT.SUBJECT}'},
            {'name': 'Message', 'value': '{ALERT.MESSAGE}'}
        ],
        'script': discord_script,
        'process_tags': '0'
    }
    
    if discord_mt:
        discord_params['mediatypeid'] = discord_mt[0]['mediatypeid']
        zabbix_request('mediatype.update', discord_params, auth_token)
        print("Updated Discord Media Type")
        discord_id = discord_mt[0]['mediatypeid']
    else:
        res = zabbix_request('mediatype.create', discord_params, auth_token)
        discord_id = res['mediatypeids'][0]
        print("Created Discord Media Type")

    # 4. Update Admin User Media
    users = zabbix_request('user.get', {'filter': {'username': 'Admin'}, 'selectMedias': 'extend'}, auth_token)
    if users:
        admin_id = users[0]['userid']
        medias = [
            {'mediatypeid': email_id, 'sendto': [EMAIL_USER], 'active': 0, 'severity': 63, 'period': '1-7,00:00-24:00'},
            {'mediatypeid': discord_id, 'sendto': ['Discord'], 'active': 0, 'severity': 63, 'period': '1-7,00:00-24:00'}
        ]
        zabbix_request('user.update', {'userid': admin_id, 'medias': medias}, auth_token)
        print("Updated Admin user media")

    # 5. Create Web Scenario & Trigger for "> 5 seconds"
    hosts = zabbix_request('host.get', {'filter': {'host': 'Zabbix server'}}, auth_token)
    if hosts:
        host_id = hosts[0]['hostid']
        # Create web scenario
        httptests = zabbix_request('httptest.get', {'filter': {'name': 'Food App Performance'}}, auth_token)
        if not httptests:
            zabbix_request('httptest.create', {
                'name': 'Food App Performance',
                'hostid': host_id,
                'delay': '30s',
                'steps': [
                    {
                        'name': 'Homepage',
                        'url': 'http://172.18.0.3:8501', # Using docker internal IP or host IP
                        'status_codes': '200',
                        'no': 1
                    }
                ]
            }, auth_token)
            print("Created HTTP Test for Food App")
        
        # Create Trigger > 5s
        triggers = zabbix_request('trigger.get', {'filter': {'description': 'Food App is too slow (> 5s)'}}, auth_token)
        if not triggers:
            zabbix_request('trigger.create', {
                'description': 'Food App is too slow (> 5s)',
                'expression': f'last(/Zabbix server/web.test.time[Food App Performance,Homepage,resp])>5',
                'priority': 4 # High
            }, auth_token)
            print("Created Trigger for slow performance")
            
        triggers_down = zabbix_request('trigger.get', {'filter': {'description': 'Food App is DOWN'}}, auth_token)
        if not triggers_down:
            zabbix_request('trigger.create', {
                'description': 'Food App is DOWN',
                'expression': f'last(/Zabbix server/web.test.fail[Food App Performance])<>0',
                'priority': 5 # Disaster
            }, auth_token)
            print("Created Trigger for downtime")

    # 6. Action to send message
    actions = zabbix_request('action.get', {'filter': {'name': 'Alert Discord and Email'}}, auth_token)
    if not actions:
        zabbix_request('action.create', {
            'name': 'Alert Discord and Email',
            'eventsource': 0,
            'status': 0,
            'esc_period': '1m',
            'filter': {
                'evaltype': 0,
                'conditions': [
                    {'conditiontype': 3, 'operator': 2, 'value': 'Food App'} # Trigger name contains "Food App"
                ]
            },
            'operations': [
                {
                    'operationtype': 0,
                    'opmessage': {
                        'default_msg': 1,
                        'mediatypeid': 0 # all
                    },
                    'opmessage_usr': [
                        {'userid': admin_id}
                    ]
                }
            ]
        }, auth_token)
        print("Created Action for Alerts")

    print("Zabbix Configuration Complete.")

if __name__ == '__main__':
    main()

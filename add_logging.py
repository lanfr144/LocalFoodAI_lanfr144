import os

files_to_update = ['scripts/setup_deploy.py', 'docker-compose.yml', 'docker/zabbix/docker-compose.yml']
log_config = '''restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"'''

for file_path in files_to_update:
    if not os.path.exists(file_path): 
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'logging:' not in content:
        content = content.replace('restart: always', log_config)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

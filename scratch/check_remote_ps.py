import os
import sys
import paramiko
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(dotenv_path=os.path.join(repo_root, ".env"))

host = os.environ.get('SERVER_HOST')
user = os.environ.get('SERVER_USER')
password = os.environ.get('SERVER_PASS')
if password == "your_db_password_here" or not password:
    password = None

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(host, username=user, password=password, timeout=10)
    print("SSH Connected!")
    
    print("--- Running Containers ---")
    stdin, stdout, stderr = ssh.exec_command("docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Command}}'")
    print(stdout.read().decode('utf-8'))
    
    print("--- Streamlit App Logs ---")
    db_cmd = "docker logs --tail 100 food_project-app-1"
    stdin, stdout, stderr = ssh.exec_command(db_cmd)
    print(stdout.read().decode('utf-8'))
    print(stderr.read().decode('utf-8'))
    
    print("--- Ingest Container Logs ---")
    stdin, stdout, stderr = ssh.exec_command("docker ps -a --filter name=food_project-ingest-run -q | xargs -I {} docker logs {}")
    print(stdout.read().decode('utf-8'))
    print(stderr.read().decode('utf-8'))
    
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()

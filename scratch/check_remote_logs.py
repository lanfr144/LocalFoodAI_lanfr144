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
    
    # Get last 50 lines of ingest run logs
    print("--- Ingest Container Logs ---")
    stdin, stdout, stderr = ssh.exec_command("docker logs food_project-ingest-run-0c5b52a70d2d")
    print(stdout.read().decode('utf-8', errors='ignore'))
    print(stderr.read().decode('utf-8', errors='ignore'))
    
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()

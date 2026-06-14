import os
import paramiko
import dotenv

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv(dotenv_path=os.path.join(repo_root, ".env"))

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
    
    cmd = "df -h"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("STDOUT:\n", stdout.read().decode('utf-8'))
    print("STDERR:\n", stderr.read().decode('utf-8'))
    
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()

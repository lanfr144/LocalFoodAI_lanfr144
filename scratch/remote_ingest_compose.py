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
    
    # Run ingestion using docker-compose run to mount data/
    print("Running ingest via docker-compose...")
    cmd = "cd food_project && docker-compose run --rm -e PYTHONIOENCODING=utf-8 ingest python -X utf8 /app/ingest_csv.py"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    # Capture outputs
    out_ing = stdout.read().decode('utf-8', errors='ignore')
    err_ing = stderr.read().decode('utf-8', errors='ignore')
    
    # Print safely
    print("STDOUT:\n", out_ing.encode('ascii', 'replace').decode('ascii'))
    print("STDERR:\n", err_ing.encode('ascii', 'replace').decode('ascii'))
    
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()

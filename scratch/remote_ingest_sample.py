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
    
    # Run ingestion inside container with forced UTF-8 encoding
    print("Running ingest_csv.py inside container...")
    cmd_ingest = "docker exec -e DB_HOST=mysql -e DB_USER=food_loader -e DB_PASS=BTSai123 -e PYTHONIOENCODING=utf-8 food_project-app-1 python -X utf8 /app/ingest_csv.py"
    stdin, stdout, stderr = ssh.exec_command(cmd_ingest)
    
    # Capture outputs
    out_ing = stdout.read().decode('utf-8', errors='ignore')
    err_ing = stderr.read().decode('utf-8', errors='ignore')
    
    # Print safely
    print("INGEST STDOUT:\n", out_ing.encode('ascii', 'replace').decode('ascii'))
    print("INGEST STDERR:\n", err_ing.encode('ascii', 'replace').decode('ascii'))
    
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()

import os
import sys
import paramiko
import dotenv
import time

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

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
    
    # 1. Kill any existing ingest-run container
    print("Killing any hung ingest containers...")
    ssh.exec_command("docker ps -a --filter name=food_project-ingest-run -q | xargs -r docker rm -f")
    
    # 2. Stop the Streamlit app container to guarantee no locks
    print("Stopping app container...")
    stdin, stdout, stderr = ssh.exec_command("cd food_project && docker-compose stop app")
    stdout.read()
    
    # 3. Restart MySQL to drop any orphaned connections or locks
    print("Restarting MySQL...")
    stdin, stdout, stderr = ssh.exec_command("cd food_project && docker-compose restart mysql")
    stdout.read()
    
    print("Waiting 10 seconds for MySQL to be healthy...")
    time.sleep(10)
    
    # 4. Run the ingestion pipeline
    print("Running database ingestion...")
    cmd = "cd food_project && docker-compose run --rm -e PYTHONIOENCODING=utf-8 ingest python -X utf8 /app/ingest_csv.py"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    # Wait for completion and read output
    out_ing = stdout.read().decode('utf-8', errors='ignore')
    err_ing = stderr.read().decode('utf-8', errors='ignore')
    
    print("INGESTION STDOUT:\n", out_ing)
    print("INGESTION STDERR:\n", err_ing)
    
    # 5. Start Streamlit app container back up
    print("Starting app container back up...")
    stdin, stdout, stderr = ssh.exec_command("cd food_project && docker-compose start app")
    stdout.read()
    
    print("Ingestion flow completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()

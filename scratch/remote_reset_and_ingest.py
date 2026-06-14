import os
import paramiko
import dotenv
import time

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
    
    # 1. Kill the hung ingest run container
    print("Cleaning up hung ingest container...")
    ssh.exec_command("docker rm -f food_project-ingest-run-0c5b52a70d2d")
    
    # 2. Restart MySQL and Streamlit App to release metadata locks
    print("Restarting MySQL to release table locks...")
    stdin, stdout, stderr = ssh.exec_command("cd food_project && docker-compose restart mysql")
    stdout.read()
    
    print("Restarting Streamlit App to reset connection pool...")
    stdin, stdout, stderr = ssh.exec_command("cd food_project && docker-compose restart app")
    stdout.read()
    
    print("Waiting 10 seconds for database health...")
    time.sleep(10)
    
    # 3. Run the ingestion pipeline
    print("Re-running database ingestion...")
    cmd = "cd food_project && docker-compose run --rm -e PYTHONIOENCODING=utf-8 ingest python -X utf8 /app/ingest_csv.py"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    # Capture outputs
    out_ing = stdout.read().decode('utf-8', errors='ignore')
    err_ing = stderr.read().decode('utf-8', errors='ignore')
    
    print("STDOUT:\n", out_ing.encode('ascii', 'replace').decode('ascii'))
    print("STDERR:\n", err_ing.encode('ascii', 'replace').decode('ascii'))
    
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()

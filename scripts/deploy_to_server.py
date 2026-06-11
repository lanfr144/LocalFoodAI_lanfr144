#!/usr/bin/env python3
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import sys
import paramiko
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def deploy():
    # Load .env
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(repo_root, ".env")
    load_dotenv(dotenv_path=env_path)

    host = os.environ.get('SERVER_HOST')
    user = os.environ.get('SERVER_USER')
    password = os.environ.get('SERVER_PASS')

    if not all([host, user]):
        print("Error: Server credentials not found in .env file.")
        return

    if password == "your_db_password_here" or password == "your_password_here" or not password:
        password = None

    print(f"Connecting to {user}@{host}...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password, timeout=10)
        print("Connected successfully!")
        
        command = "cd food_project && rm -f git_version.txt git_id.txt && git pull && docker-compose up -d --build"
        print(f"Executing: {command}")
        
        stdin, stdout, stderr = ssh.exec_command(command)
        
        out = stdout.read().decode('utf-8')
        err = stderr.read().decode('utf-8')
        
        if out: print(f"Output:\n{out}")
        if err: print(f"Errors:\n{err}")
        
    except Exception as e:
        print(f"Failed to connect or execute command: {e}")
    finally:
        ssh.close()
        print("Connection closed.")

if __name__ == "__main__":
    deploy()
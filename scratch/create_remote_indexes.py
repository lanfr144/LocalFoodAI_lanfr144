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
    
    queries = [
        "ALTER TABLE food_db.products_core ADD FULLTEXT INDEX idx_prod_ing (product_name, ingredients_text);",
        "ALTER TABLE food_db.products_core ADD FULLTEXT INDEX idx_prod_name (product_name);",
        "ALTER TABLE food_db.products_core ADD FULLTEXT INDEX idx_ing_text (ingredients_text);"
    ]
    
    for q in queries:
        print(f"Executing: {q}")
        cmd = f"docker exec food_project-mysql-1 mysql -uroot -pBTSai123 -e '{q}'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("STDOUT:\n", stdout.read().decode('utf-8'))
        print("STDERR:\n", stderr.read().decode('utf-8'))
        
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()

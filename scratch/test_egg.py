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
    
    python_cmd = """
import ollama
import json
model = 'llama3.2:3b'

unique_aliments = ["Egg"]
aliments_str = ", ".join(unique_aliments)
prompt = f"In these aliments : {aliments_str} are there allergens and if it is the case also said the allergen kinds. Return the answer as json array with two variables aliment and the associate allergen in an array find inside it. focus on the list, do not add or delete aliments."

try:
    response = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        format='json'
    )
    res_content = response['message']['content'].strip()
    print("Response Content:\\n", res_content)
    
    data = json.loads(res_content)
    print("Parsed JSON:\\n", json.dumps(data, indent=2))
except Exception as e:
    print("Error:", e)
"""
    
    sftp = ssh.open_sftp()
    with sftp.file('food_project/test_egg.py', 'w') as f:
        f.write(python_cmd)
    sftp.close()
    
    ssh.exec_command("docker cp food_project/test_egg.py food_project-app-1:/app/test_egg.py")
    
    stdin, stdout, stderr = ssh.exec_command("docker exec food_project-app-1 python /app/test_egg.py")
    print("STDOUT:\n", stdout.read().decode('utf-8'))
    print("STDERR:\n", stderr.read().decode('utf-8'))
    
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()

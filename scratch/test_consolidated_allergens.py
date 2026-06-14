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
model = 'llama3.2:3b'

candidates = ["milk chocolate", "peanuts", "sugar", "milk", "cocoa butter", "lactose", "snickers bar", "snickers"]

prompt_lines = [
    "You are a food safety expert. For each item in the list below, answer the question exactly.",
    "Respond with 'Yes' or 'No'. Format the output exactly as:",
    "ItemName: Yes/No",
    "\\nQuestions:"
]

for c in candidates:
    prompt_lines.append(f"Answer by yes or no, if it is in some case answer yes : Are {c} allergens.")

prompt = "\\n".join(prompt_lines)

print("--- Sending Consolidated Prompt ---")
import time
t0 = time.time()
res = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
content = res['message']['content'].strip()
print("Response:\\n", content)
print("Time taken:", time.time() - t0)
"""
    
    # Write python_cmd to server
    sftp = ssh.open_sftp()
    with sftp.file('food_project/test_consolidated.py', 'w') as f:
        f.write(python_cmd)
    sftp.close()
    
    # Copy to container
    ssh.exec_command("docker cp food_project/test_consolidated.py food_project-app-1:/app/test_consolidated.py")
    
    stdin, stdout, stderr = ssh.exec_command("docker exec food_project-app-1 python /app/test_consolidated.py")
    print("STDOUT:\\n", stdout.read().decode('utf-8'))
    print("STDERR:\\n", stderr.read().decode('utf-8'))
    
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()

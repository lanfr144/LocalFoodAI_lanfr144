import os
import sys
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
    
    # Run a test inside the container
    python_cmd = """
import ollama
model = 'llama3.2:3b'

# Test product: Peanut butter with milk
name = "Snickers Bar"
ingredients = "milk chocolate, peanuts, sugar, milk, cocoa butter, lactose"
allergens = [
    "Peanuts", "Eggs", "Milk", "Wheat", "Gluten", "Soy", 
    "Tree Nuts", "Fish", "Shellfish", "Sesame", "Mustard", 
    "Celery", "Lupin", "Molluscs", "Sulphites"
]

print("--- Testing Loop ---")
import time
t0 = time.time()
detected = []
# Just test first 3 allergens in loop to measure time
for allergen in allergens[:3]:
    prompt = f'Answer by yes or no, if it is in some case answer yes : Are {allergen} allergens in the product "{name}" with ingredients "{ingredients}"?'
    res = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
    ans = res['message']['content'].strip()
    print(f"{allergen}: {ans}")
    if 'yes' in ans.lower():
        detected.append(allergen)
print("Loop time for 3:", time.time() - t0)

print("\\n--- Testing Single Call ---")
t0 = time.time()
prompt = f'''Given the product "{name}" with ingredients "{ingredients}".
For each allergen in the list: Peanuts, Eggs, Milk, Wheat, Gluten, Soy, Tree Nuts, Fish, Shellfish, Sesame, Mustard, Celery, Lupin, Molluscs, Sulphites.
Answer by yes or no, if it is in some case answer yes: Are they allergens in this product?
Format your response exactly as:
AllergenName: Yes/No
'''
res = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
print(res['message']['content'].strip())
print("Single call time:", time.time() - t0)
"""
    
    # Write python_cmd to a temporary file on the server and copy to container
    sftp = ssh.open_sftp()
    with sftp.file('food_project/test_ollama.py', 'w') as f:
        f.write(python_cmd)
    sftp.close()
    
    # Copy file into container
    ssh.exec_command("docker cp food_project/test_ollama.py food_project-app-1:/app/test_ollama.py")
    
    stdin, stdout, stderr = ssh.exec_command("docker exec food_project-app-1 python /app/test_ollama.py")
    print("STDOUT:\n", stdout.read().decode('utf-8'))
    print("STDERR:\n", stderr.read().decode('utf-8'))
    
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()

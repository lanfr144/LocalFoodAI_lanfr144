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

unique_aliments = [
    "peanut butter honey biscuits with peanut butter filling",
    "1% milk fat low fat milk",
    "peanut butter",
    "honey",
    "biscuits",
    "peanut",
    "butter",
    "filling",
    "1%",
    "milk",
    "fat",
    "low"
]
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
    
    # Robust dictionary-or-list JSON parser
    aliments_array = []
    if isinstance(data, list):
        aliments_array = data
    elif isinstance(data, dict):
        for val in data.values():
            if isinstance(val, list):
                aliments_array = val
                break
                
    table_data = []
    if aliments_array:
        for entry in aliments_array:
            if isinstance(entry, dict):
                aliment = entry.get('aliment')
                allergens = entry.get('allergen') or entry.get('allergens') or []
                if aliment:
                    if isinstance(allergens, list) and allergens:
                        cleaned_algs = [str(alg).strip().title() for alg in allergens if alg]
                        table_data.append({
                            "Aliment (Ingredient)": aliment.strip().title(),
                            "Allergen Kind(s)": ", ".join(cleaned_algs)
                        })
                    elif isinstance(allergens, str) and allergens.strip():
                        table_data.append({
                            "Aliment (Ingredient)": aliment.strip().title(),
                            "Allergen Kind(s)": allergens.strip().title()
                        })
    print("Table Data:\\n", table_data)
except Exception as e:
    print("Error:", e)
"""
    
    sftp = ssh.open_sftp()
    with sftp.file('food_project/test_plate_json.py', 'w') as f:
        f.write(python_cmd)
    sftp.close()
    
    ssh.exec_command("docker cp food_project/test_plate_json.py food_project-app-1:/app/test_plate_json.py")
    
    stdin, stdout, stderr = ssh.exec_command("docker exec food_project-app-1 python /app/test_plate_json.py")
    print("STDOUT:\n", stdout.read().decode('utf-8'))
    print("STDERR:\n", stderr.read().decode('utf-8'))
    
except Exception as e:
    print(f"Error: {e}")
finally:
    ssh.close()

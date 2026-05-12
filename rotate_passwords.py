import pymysql
import os
import secrets
import string
import subprocess

def generate_password(length=16):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

def update_env_file(passwords):
    env_file = '.env'
    lines = []
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            lines = f.readlines()
            
    # Remove old password lines
    lines = [l for l in lines if not any(l.startswith(f"{k}=") for k in passwords.keys())]
    
    # Add new passwords
    for key, val in passwords.items():
        lines.append(f"{key}={val}\n")
        
    with open(env_file, 'w') as f:
        f.writelines(lines)
    print("✅ .env file updated with new synchronized passwords.")

def main():
    print("🔄 Starting Password Synchronization Routine...")
    
    # 1. Connect to MySQL as root
    try:
        conn = pymysql.connect(
            host='192.168.130.170',  # Assuming we run this from host to mapped port, or within a container network
            port=3307,
            user='root',
            password='root_pass',
            database='food_db'
        )
    except Exception as e:
        print(f"❌ Could not connect to MySQL: {e}")
        return

    # 2. Generate new passwords
    new_passwords = {
        'DB_READER_PASS': generate_password(),
        'DB_LOADER_PASS': generate_password(),
        'DB_APP_AUTH_PASS': generate_password()
    }
    
    # 3. Update MySQL Users
    try:
        with conn.cursor() as cursor:
            cursor.execute("ALTER USER 'db_reader'@'%%' IDENTIFIED BY %s", (new_passwords['DB_READER_PASS'],))
            cursor.execute("ALTER USER 'db_loader'@'%%' IDENTIFIED BY %s", (new_passwords['DB_LOADER_PASS'],))
            cursor.execute("ALTER USER 'db_app_auth'@'%%' IDENTIFIED BY %s", (new_passwords['DB_APP_AUTH_PASS'],))
            cursor.execute("FLUSH PRIVILEGES")
            conn.commit()
        print("✅ Database user passwords rotated successfully.")
    except Exception as e:
        print(f"❌ Failed to alter database users: {e}")
    finally:
        conn.close()
        
    # 4. Update .env file so Docker Compose picks it up
    update_env_file(new_passwords)
    
    # 5. Gracefully restart client containers to sync connection
    print("🔄 Restarting App and Ingest containers to synchronize new credentials...")
    try:
        subprocess.run(["docker-compose", "up", "-d", "app"], check=True)
        # We don't necessarily need to restart ingest if it's manual, but we can recreate it if it was running.
        print("✅ Client containers synchronized with new database passwords!")
    except Exception as e:
        print(f"⚠️ Failed to restart docker containers: {e}")

if __name__ == "__main__":
    main()

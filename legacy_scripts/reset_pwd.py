import bcrypt
import pymysql
import sys

import myloginpath

def get_db_connection():
    conf = myloginpath.parse('app_auth')
    return pymysql.connect(
        host=conf.get('host', '127.0.0.1'),
        user=conf.get('user', 'db_app_auth'),
        password=conf.get('password'),
        database='food_db',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def reset_pwd(username, plain_password):
    conn = get_db_connection()
    if not conn:
        print("Failed DB connection!")
        sys.exit(1)
        
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    with conn.cursor() as cursor:
        rows = cursor.execute("UPDATE users SET password_hash = %s WHERE username = %s", (hashed, username))
        if rows > 0:
            print(f"✅ Successfully updated password for {username}!")
        else:
            print(f"❌ User '{username}' not found in database!")
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        username = input("Enter Username: ")
        plain_password = input("Enter New Password: ")
    else:
        username = sys.argv[1]
        plain_password = sys.argv[2]
        
    reset_pwd(username, plain_password)

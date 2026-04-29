import bcrypt
import myloginpath
import pymysql

def test_login(username, password):
    conf = myloginpath.parse('app_auth')
    conn = pymysql.connect(
        host=conf.get('host', '127.0.0.1'),
        user=conf.get('user'),
        password=conf.get('password'),
        database='food_db',
        cursorclass=pymysql.cursors.DictCursor
    )
    with conn.cursor() as cursor:
        cursor.execute("SELECT password_hash FROM users WHERE username = %s LIMIT 1", (username,))
        result = cursor.fetchone()
    conn.close()
    if result:
        return bcrypt.checkpw(password.encode('utf-8'), result['password_hash'].encode('utf-8'))
    return False

# Try registering a user and testing it
def register_and_test():
    conf = myloginpath.parse('app_auth')
    conn = pymysql.connect(
        host=conf.get('host', '127.0.0.1'),
        user=conf.get('user'),
        password=conf.get('password'),
        database='food_db',
        cursorclass=pymysql.cursors.DictCursor
    )
    username = "test_bot"
    password = "bot_password"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)", (username, hashed, 'bot@bot.com'))
            conn.commit()
    except Exception as e:
        print("Insert failed:", e)
    conn.close()
    
    print("Login successful?", test_login(username, password))

if __name__ == "__main__":
    register_and_test()

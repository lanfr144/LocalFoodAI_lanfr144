import myloginpath
import pymysql
import bcrypt

conf = myloginpath.parse('app_auth')
conn = pymysql.connect(
    host=conf.get('host', '127.0.0.1'),
    user=conf.get('user'),
    password=conf.get('password'),
    database='food_db',
    cursorclass=pymysql.cursors.DictCursor
)

with conn.cursor() as c:
    c.execute("SELECT * FROM users;")
    users = c.fetchall()

for u in users:
    print("User:", u['username'], "Hash:", u['password_hash'])

# Check Admin password
with conn.cursor() as c:
    c.execute("SELECT * FROM users WHERE username='Admin'")
    admin = c.fetchone()
    if admin:
        print("Admin check BTSai123:", bcrypt.checkpw(b'BTSai123', admin['password_hash'].encode('utf-8')))

conn.close()

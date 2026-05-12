import os
import pymysql

def get_db_connection():
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_user = os.environ.get('DB_READER_USER', 'db_reader')
    db_pass = os.environ.get('DB_READER_PASS', 'reader_pass')
    return pymysql.connect(host=db_host, user=db_user, password=db_pass, database='food_db', cursorclass=pymysql.cursors.DictCursor)

conn = get_db_connection()
with conn.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) as c FROM food_db.products_core")
    print("Total Core Rows:", cursor.fetchone()['c'])
    
    sq = "white rice"
    bool_search = " ".join([f"+{w}" for w in sq.split()])
    print("Search query:", bool_search)
    
    sql = """
    SELECT code, product_name 
    FROM food_db.products_core
    WHERE MATCH(product_name, ingredients_text) AGAINST(%s IN BOOLEAN MODE)
    LIMIT 5
    """
    cursor.execute(sql, (bool_search,))
    res = cursor.fetchall()
    print("Result (MATCH product_name, ingredients_text):", len(res))
    
    # Check if MATCH(product_name) works instead
    sql = """
    SELECT code, product_name 
    FROM food_db.products_core
    WHERE product_name LIKE %s
    LIMIT 5
    """
    cursor.execute(sql, (f"%{sq}%",))
    res2 = cursor.fetchall()
    print("Result (LIKE):", len(res2))
conn.close()

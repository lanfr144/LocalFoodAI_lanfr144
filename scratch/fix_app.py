import re
import os

file_path = "app.py"
with open(file_path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# Replace encoding issues
content = content.replace("Lange Franois", "Francois Lange")
content = content.replace("Lange FranA ois", "Francois Lange")

# 1. Update get_db_connection
old_db_conn = """def get_db_connection(login_path):
    try:
        import os
        db_host = os.environ.get('DB_HOST')
        # Check if environment variables exist for this login path
        db_user = os.environ.get(f'{login_path.upper()}_USER') or os.environ.get('DB_USER')
        db_pass = os.environ.get(f'{login_path.upper()}_PASS') or os.environ.get('DB_PASS')

        if db_host and db_user and db_pass:
            return pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_pass,
                database='food_db',
                cursorclass=pymysql.cursors.DictCursor
            )
            
        conf = myloginpath.parse(login_path)
        if not conf or not conf.get('user'):
            st.error(f"⚠️ MySQL configuration missing for `{login_path}`. If you are testing locally on Windows, this app must be run on the Ubuntu server where `mysql_config_editor` is properly configured.")
            return None
            
        return pymysql.connect(
            host=conf.get('host', '127.0.0.1'),
            user=conf.get('user'),
            password=conf.get('password'),
            database='food_db',
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        st.error(f"Connection Failed: {e}")
        return None"""

new_db_conn = """def get_db_connection(login_path):
    try:
        import os
        db_host = os.environ.get('DB_HOST')
        # Check if environment variables exist for this login path
        db_user = os.environ.get(f'{login_path.upper()}_USER') or os.environ.get('DB_USER')
        db_pass = os.environ.get(f'{login_path.upper()}_PASS') or os.environ.get('DB_PASS')

        if db_host and db_user and db_pass:
            return pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_pass,
                database='food_db',
                cursorclass=pymysql.cursors.DictCursor
            )
            
        conf = myloginpath.parse(login_path)
        if not conf or not conf.get('user'):
            st.error(f"⚠️ MySQL configuration missing for `{login_path}`. If you are testing locally on Windows, this app must be run on the Ubuntu server where `mysql_config_editor` is properly configured.")
            notifier.send_alert(f"MySQL Config Missing: {login_path}")
            return None
            
        return pymysql.connect(
            host=conf.get('host', '127.0.0.1'),
            user=conf.get('user'),
            password=conf.get('password'),
            database='food_db',
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        st.error(f"Connection Failed: {e}")
        notifier.send_alert(f"Database Connection Failed ({login_path}): {e}")
        return None"""

content = content.replace(old_db_conn, new_db_conn)

# 2. Update db_cursor
old_db_cursor = """@contextmanager
def db_cursor(login_path: str):
    conn = get_db_connection(login_path)
    if not conn:
        yield None
        return
    try:
        with conn.cursor() as cursor:
            yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        st.error(f"Database query error: {e}")
        raise e
    finally:
        conn.close()"""

new_db_cursor = """@contextmanager
def db_cursor(login_path: str):
    conn = get_db_connection(login_path)
    if not conn:
        yield None
        return
    try:
        with conn.cursor() as cursor:
            yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        st.error(f"Database query error: {e}")
        notifier.send_alert(f"Database Query Error ({login_path}): {e}")
        raise e
    finally:
        conn.close()"""

content = content.replace(old_db_cursor, new_db_cursor)

# 3. Update query_plate_allergens exception
content = content.replace(
    "    except Exception:\n        pass\n    return table_data",
    "    except Exception as e:\n        notifier.send_alert(f\"LLM query_plate_allergens error: {e}\")\n        pass\n    return table_data"
)

# 4. Update detect_allergens_from_text exception
content = content.replace(
    "    except Exception:\n        pass\n    return detected",
    "    except Exception as e:\n        notifier.send_alert(f\"LLM detect_allergens_from_text error: {e}\")\n        pass\n    return detected"
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("app.py successfully updated and encoding sanitized.")

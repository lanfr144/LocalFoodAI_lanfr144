import pymysql
import getpass
import os

def run_db_setup():
    """ 
    This Python script prompts for passwords securely and executes CREATE USER / GRANT 
    statements to provision the MySQL server dynamically without config files.
    """
    print("Welcome to Local Food AI Initial Setup.")
    print("WARNING: This will configure your MySQL server. You must know the MySQL root password.\n")
    
    root_password = getpass.getpass("Enter the MySQL 'root' password: ")
    
    # Prompt for the new user passwords (so they aren't stored anywhere!)
    print("\nPlease define the passwords for the service accounts:")
    owner_pass = getpass.getpass("  1. Enter password for 'db_owner': ")
    reader_pass = getpass.getpass("  2. Enter password for 'db_reader' (Used by Web UI): ")
    loader_pass = getpass.getpass("  3. Enter password for 'db_loader' (Used by Scripts): ")
    app_auth_pass = getpass.getpass("  4. Enter password for 'db_app_auth' (Used for User Login): ")

    print("\nConnecting as root to configure server...")
    try:
        conn = pymysql.connect(
            host='127.0.0.1',  # Local host execution context
            user='root',
            password=root_password,
            autocommit=True
        )
        cursor = conn.cursor()
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    queries = [
        "CREATE DATABASE IF NOT EXISTS food_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
        
        # Owner User
        f"CREATE USER IF NOT EXISTS 'db_owner'@'%' IDENTIFIED BY '{owner_pass}';",
        "GRANT ALL PRIVILEGES ON food_db.* TO 'db_owner'@'%' WITH GRANT OPTION;",
        
        # Reader User
        f"CREATE USER IF NOT EXISTS 'db_reader'@'%' IDENTIFIED BY '{reader_pass}';",
        "GRANT USAGE ON *.* TO 'db_reader'@'%';",
        
        # Loader User
        f"CREATE USER IF NOT EXISTS 'db_loader'@'%' IDENTIFIED BY '{loader_pass}';",
        "GRANT USAGE ON *.* TO 'db_loader'@'%';",
        "GRANT FILE ON *.* TO 'db_loader'@'%';",  
        
        # App Auth User (PoLP)
        f"CREATE USER IF NOT EXISTS 'db_app_auth'@'%' IDENTIFIED BY '{app_auth_pass}';",
        "GRANT USAGE ON *.* TO 'db_app_auth'@'%';",
        
        "FLUSH PRIVILEGES;"
    ]

    for q in queries:
        print(f"Executing: {q[:60]}...")
        cursor.execute(q)

    # Now create the table logic safely
    print("\nCreating Tables and Granting Table-Specific Access...")
    
    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_db.users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """)
    # 2. Products Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_db.products (
        code VARCHAR(50) PRIMARY KEY, url TEXT, creator VARCHAR(255), created_t VARCHAR(50), 
        created_datetime VARCHAR(50), last_modified_t VARCHAR(50), last_modified_datetime VARCHAR(50), 
        product_name TEXT, generic_name TEXT, quantity VARCHAR(255), packaging TEXT, brands TEXT, 
        categories TEXT, origins TEXT, labels TEXT, stores TEXT, countries TEXT, ingredients_text TEXT, 
        allergens TEXT, traces TEXT, 
        FULLTEXT INDEX ft_idx_search (product_name, ingredients_text)
    ) ENGINE=InnoDB;
    """)
    
    # Table Context Grants (SoD)
    cursor.execute("GRANT SELECT, INSERT, UPDATE ON food_db.users TO 'db_app_auth'@'%';")
    cursor.execute("GRANT SELECT ON food_db.products TO 'db_reader'@'%';")
    cursor.execute("GRANT SELECT, INSERT, UPDATE, DELETE, DROP, CREATE ON food_db.products TO 'db_loader'@'%';")
    cursor.execute("FLUSH PRIVILEGES;")

    print("\n✅ Database, Users, and Tables created successfully!")
    cursor.close()
    conn.close()

    print("\n🎉 Setup Complete.")
    print("\n!!! IMPORTANT NEXT STEPS !!!")
    print("Now, use `mysql_config_editor` to store these passwords locally so the app can use them:")
    print("  mysql_config_editor set --login-path=app_reader --host=127.0.0.1 --user=db_reader --password")
    print("  mysql_config_editor set --login-path=app_auth --host=127.0.0.1 --user=db_app_auth --password")

if __name__ == "__main__":
    run_db_setup()

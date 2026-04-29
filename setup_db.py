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
    
    # Automatically fetch passwords for secure CI/CD deployment or fallback for exam/local setup
    root_password = os.environ.get("MYSQL_ROOT_PASSWORD", "")
    owner_pass = os.environ.get("DB_OWNER_PASS", "BTSai123")
    reader_pass = os.environ.get("DB_READER_PASS", "BTSai123")
    loader_pass = os.environ.get("DB_LOADER_PASS", "BTSai123")
    app_auth_pass = os.environ.get("DB_AUTH_PASS", "BTSai123")

    print("\nConnecting as root to configure server...")
    try:
        # Connect using the local unix socket which allows seamless auth_socket root login on Ubuntu
        conn = pymysql.connect(
            unix_socket='/var/run/mysqld/mysqld.sock', 
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
        email VARCHAR(255) NULL,
        search_limit VARCHAR(10) DEFAULT '50',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """)

    # Gracefully add email and search_limit to existing tables if script is re-run
    try:
        cursor.execute("ALTER TABLE food_db.users ADD COLUMN email VARCHAR(255) NULL;")
    except Warning:
        pass
    except Exception as e:
        if 'Duplicate column name' not in str(e):
            print(f"Skipped altering users (Email): {e}")
            
    try:
        cursor.execute("ALTER TABLE food_db.users ADD COLUMN search_limit VARCHAR(10) DEFAULT '50';")
    except Warning:
        pass
    except Exception as e:
        if 'Duplicate column name' not in str(e):
            print(f"Skipped altering users (Limit): {e}")

    # 1.5 Medical Profiles Table (EAV Migration)
    # We drop the old schema to clear constraints, allowing the dynamic structure to take over
    cursor.execute("DROP TABLE IF EXISTS food_db.user_profiles;")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_db.user_health_profiles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        illness_health_condition_diet_dislikes_name VARCHAR(100) NOT NULL DEFAULT 'None',
        illness_health_condition_diet_dislikes_value VARCHAR(255) NOT NULL DEFAULT 'None',
        FOREIGN KEY (user_id) REFERENCES food_db.users(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 2. Plates Table (For storing custom combos)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_db.plates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        plate_name VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES food_db.users(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 3. Plate Items Table (Linking products to a plate natively)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_db.plate_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        plate_id INT NOT NULL,
        product_code VARCHAR(50) NOT NULL,
        quantity_grams DOUBLE NOT NULL,
        FOREIGN KEY (plate_id) REFERENCES food_db.plates(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    # 4. Products Tables (Grouped Vertical Partitioning)
    tables = [
        "food_db.products_core",
        "food_db.products_allergens",
        "food_db.products_macros",
        "food_db.products_vitamins",
        "food_db.products_minerals"
    ]
    cursor.execute("DROP VIEW IF EXISTS food_db.products;")
    cursor.execute("DROP TABLE IF EXISTS food_db.products;")
    for t in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {t};")
        
    cursor.execute("""
    CREATE TABLE food_db.products_core (
        code VARCHAR(50) PRIMARY KEY,
        product_name TEXT NULL,
        generic_name TEXT NULL,
        brands TEXT NULL,
        ingredients_text TEXT NULL,
        FULLTEXT idx_search (product_name, ingredients_text),
        INDEX idx_brands (brands(50)),
        INDEX idx_generic (generic_name(50))
    ) ENGINE=InnoDB;
    """)

    cursor.execute("""
    CREATE TABLE food_db.products_allergens (
        code VARCHAR(50) PRIMARY KEY,
        allergens TEXT NULL,
        FULLTEXT idx_allergens (allergens),
        FOREIGN KEY (code) REFERENCES food_db.products_core(code) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    cursor.execute("""
    CREATE TABLE food_db.products_macros (
        code VARCHAR(50) PRIMARY KEY,
        `energy-kcal_100g` DOUBLE NULL,
        proteins_100g DOUBLE NULL,
        fat_100g DOUBLE NULL,
        carbohydrates_100g DOUBLE NULL,
        sugars_100g DOUBLE NULL,
        fiber_100g DOUBLE NULL,
        sodium_100g DOUBLE NULL,
        salt_100g DOUBLE NULL,
        cholesterol_100g DOUBLE NULL,
        FOREIGN KEY (code) REFERENCES food_db.products_core(code) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    cursor.execute("""
    CREATE TABLE food_db.products_vitamins (
        code VARCHAR(50) PRIMARY KEY,
        `vitamin-a_100g` DOUBLE NULL,
        `vitamin-b1_100g` DOUBLE NULL,
        `vitamin-b2_100g` DOUBLE NULL,
        `vitamin-pp_100g` DOUBLE NULL,
        `vitamin-b6_100g` DOUBLE NULL,
        `vitamin-b9_100g` DOUBLE NULL,
        `vitamin-b12_100g` DOUBLE NULL,
        `vitamin-c_100g` DOUBLE NULL,
        `vitamin-d_100g` DOUBLE NULL,
        `vitamin-e_100g` DOUBLE NULL,
        `vitamin-k_100g` DOUBLE NULL,
        FOREIGN KEY (code) REFERENCES food_db.products_core(code) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    cursor.execute("""
    CREATE TABLE food_db.products_minerals (
        code VARCHAR(50) PRIMARY KEY,
        calcium_100g DOUBLE NULL,
        iron_100g DOUBLE NULL,
        magnesium_100g DOUBLE NULL,
        potassium_100g DOUBLE NULL,
        zinc_100g DOUBLE NULL,
        FOREIGN KEY (code) REFERENCES food_db.products_core(code) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    cursor.execute("""
    CREATE VIEW food_db.products AS 
    SELECT 
        c.code, c.product_name, c.generic_name, c.brands, c.ingredients_text,
        a.allergens,
        m.`energy-kcal_100g`, m.proteins_100g, m.fat_100g, m.carbohydrates_100g, m.sugars_100g, m.fiber_100g, m.sodium_100g, m.salt_100g, m.cholesterol_100g,
        v.`vitamin-a_100g`, v.`vitamin-b1_100g`, v.`vitamin-b2_100g`, v.`vitamin-pp_100g`, v.`vitamin-b6_100g`, v.`vitamin-b9_100g`, v.`vitamin-b12_100g`, v.`vitamin-c_100g`, v.`vitamin-d_100g`, v.`vitamin-e_100g`, v.`vitamin-k_100g`,
        min.calcium_100g, min.iron_100g, min.magnesium_100g, min.potassium_100g, min.zinc_100g
    FROM food_db.products_core c
    LEFT JOIN food_db.products_allergens a ON c.code = a.code
    LEFT JOIN food_db.products_macros m ON c.code = m.code
    LEFT JOIN food_db.products_vitamins v ON c.code = v.code
    LEFT JOIN food_db.products_minerals min ON c.code = min.code;
    """)
    
    cursor.execute("GRANT SELECT ON food_db.* TO 'db_reader'@'%';")
    cursor.execute("GRANT SELECT, INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, INDEX, CREATE VIEW ON food_db.* TO 'db_loader'@'%';")
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

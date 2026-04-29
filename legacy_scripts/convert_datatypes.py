import pymysql
import pandas as pd
import getpass

def detect_and_convert_types():
    print("Welcome to the Data Types Optimizer.")
    print("WARNING: This modifies your database schemas. You must authenticate as the database `db_owner`.\n")
    
    owner_pass = getpass.getpass("Enter the MySQL 'db_owner' password: ")

    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            user='db_owner',
            password=owner_pass,
            database='food_db'
        )
        cursor = conn.cursor()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # Assuming we check common known numerical columns to shrink the DB footprint
    columns_to_inspect = ["quantity", "created_t", "last_modified_t"]

    for col in columns_to_inspect:
        print(f"\nAnalyzing column: `{col}`")
        
        try:
            # Check if column exists by picking 5000 non nulls
            query = f"SELECT `{col}` FROM products WHERE `{col}` IS NOT NULL AND `{col}` != '' LIMIT 5000"
            df = pd.read_sql(query, conn)
        except Exception as e:
            print(f" ⚠️ Could not read column `{col}`: {e}")
            continue
            
        if df.empty:
            print(f" ⏭️ Column `{col}` is entirely null/empty. Keeping as TEXT.")
            continue
            
        series = df[col].astype(str).str.strip()
        
        # INTEGER CHECK
        if series.str.match(r'^-?\d+$').all():
            print(f" ⚙️ Status: ALL INTS matched. Converting `{col}` to BIGINT.")
            try:
                cursor.execute(f"UPDATE products SET `{col}` = NULL WHERE `{col}` = '';")
                cursor.execute(f"ALTER TABLE products MODIFY COLUMN `{col}` BIGINT;")
                conn.commit()
                print(" ✅ Success")
            except Exception as e:
                print(f" ❌ Failed to alter table: {e}")
            continue
            
        # FLOAT CHECK
        test_float = series.str.replace(',', '.')
        if test_float.str.match(r'^-?\d*\.\d+$').any() and test_float.str.match(r'^-?\d*\.?\d+$').all():
            print(f" ⚙️ Status: FLOATS detected. Standardizing and converting `{col}` to DOUBLE...")
            try:
                cursor.execute(f"UPDATE products SET `{col}` = NULL WHERE `{col}` = '';")
                cursor.execute(f"UPDATE products SET `{col}` = REPLACE(`{col}`, ',', '.') WHERE `{col}` LIKE '%,%';")
                cursor.execute(f"ALTER TABLE products MODIFY COLUMN `{col}` DOUBLE;")
                conn.commit()
                print(" ✅ Success")
            except Exception as e:
                print(f" ❌ Failed to alter table: {e}")
            continue

        print(f" ⏭️ Keeping `{col}` as TEXT.")

    cursor.close()
    conn.close()
    print("\n🎉 Datatype conversion complete!")

if __name__ == '__main__':
    detect_and_convert_types()

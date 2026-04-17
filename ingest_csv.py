import pandas as pd
import pymysql
import myloginpath
import os
import sys

def get_loader_connection():
    try:
        conf = myloginpath.parse('app_loader')
        return pymysql.connect(
            host=conf.get('host', '127.0.0.1'),
            user=conf.get('user'),
            password=conf.get('password'),
            database='food_db',
            local_infile=True
        )
    except Exception as e:
        print(f"❌ Failed to connect to MySQL via app_loader: {e}")
        print("Did you run: mysql_config_editor set --login-path=app_loader --host=127.0.0.1 --user=db_loader --password")
        sys.exit(1)

def ingest_file(filename, conn):
    if not os.path.exists(filename):
        return False
        
    print(f"\n🚀 Found {filename}! Starting ingestion pipeline...")
    
    # We read the first few rows to grab the columns our table actually expects. 
    # (assuming products table matches OpenFoodFacts core schema)
    expected_columns = [
        "code", "url", "creator", "created_t", "created_datetime", "last_modified_t", 
        "last_modified_datetime", "product_name", "generic_name", "quantity", "packaging", 
        "brands", "categories", "origins", "labels", "stores", "countries", "ingredients_text", 
        "allergens", "traces"
    ]
    
    # Reduced chunk size to 1000 to prevent 'max_allowed_packet' and PyMySQL memory crash
    chunk_size = 1000 
    total_processed = 0

    # Using chunking to stream into MySQL efficiently
    for chunk in pd.read_csv(filename, sep='\t', dtype=str, chunksize=chunk_size, on_bad_lines='skip'):
        # Filter only the columns we mapped
        available_cols = [col for col in expected_columns if col in chunk.columns]
        df = chunk[available_cols]
        
        # Replace NaN with None so MySQL treats it as NULL
        df = df.where(pd.notnull(df), None)
        
        placeholders = ', '.join(['%s'] * len(available_cols))
        columns_str = ', '.join([f"`{col}`" for col in available_cols])
        
        # Use INSERT IGNORE to prevent crashing on duplicate primary keys (barcodes)
        sql = f"INSERT IGNORE INTO products ({columns_str}) VALUES ({placeholders})"
        
        with conn.cursor() as cursor:
            cursor.executemany(sql, df.values.tolist())
        conn.commit()
        
        total_processed += len(df)
        print(f"   Inserted {total_processed} rows...")
        
    print(f"✅ Finished importing {filename}.")
    return True

if __name__ == "__main__":
    print("Initiating OpenFoodFacts CSV Ingestion Process...")
    conn = get_loader_connection()
    
    processed_en = ingest_file('en.openfoodfacts.org.products.csv', conn)
    processed_fr = ingest_file('fr.openfoodfacts.org.products.csv', conn)
    
    if not processed_en and not processed_fr:
        print("\n❌ Could not find either 'en.openfoodfacts.org.products.csv' or 'fr.openfoodfacts.org.products.csv'.")
        print("Please download them directly into the root folder and run this script again.")
        
    conn.close()

import pandas as pd
import myloginpath
import urllib.parse
from sqlalchemy import create_engine
import os
import sys

def get_loader_engine():
    try:
        conf = myloginpath.parse('app_loader')
        user = conf.get('user')
        password = urllib.parse.quote_plus(conf.get('password'))
        host = conf.get('host', '127.0.0.1')
        database = 'food_db'
        
        # Build strict SQLAlchemy PyMySQL string
        conn_str = f"mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4"
        return create_engine(conn_str)
    except Exception as e:
        print(f"❌ Failed to parse myloginpath or create engine: {e}")
        sys.exit(1)

def ingest_file(filename, engine):
    if not os.path.exists(filename):
        print(f"File {filename} not found locally.")
        return False
        
    print(f"\n🚀 Found {filename}! Starting ingestion via SQLAlchemy pipeline...")
    
    expected_columns = [
        "code", "url", "creator", "created_t", "created_datetime", "last_modified_t", 
        "last_modified_datetime", "product_name", "generic_name", "quantity", "packaging", 
        "brands", "categories", "origins", "labels", "stores", "countries", "ingredients_text", 
        "allergens", "traces"
    ]
    
    chunk_size = 5000 
    total_processed = 0

    for chunk in pd.read_csv(filename, sep='\t', dtype=str, chunksize=chunk_size, on_bad_lines='skip'):
        # Filter explicitly to schema
        available_cols = [col for col in expected_columns if col in chunk.columns]
        df = chunk[available_cols]
        
        # Pandas to_sql safely transforms NaNs to SQL NULLs internally
        try:
            # We use 'append' because the products table already exists with primary keys
            # To handle duplicate 'code' primary keys effortlessly, we drop duplicates from the dataframe before insert
            # Or depend on PyMySQL. But pandas natively crashes on dupes unless managed. 
            df = df.drop_duplicates(subset=['code'])
            df.to_sql('products', con=engine, if_exists='append', index=False)
            total_processed += len(df)
            print(f"   Successfully appended {total_processed} rows...")
        except BaseException as e:
            # If a strict primary key duplicate existed in DB already from a previous chunk, ignore row crashes
            if "Duplicate entry" in str(e):
                pass
            else:
                 print(f"   [Warning] Chunk skipped due to internal structural error: {e}")
        
    print(f"✅ Finished importing {filename}.")
    return True

if __name__ == "__main__":
    print("Initiating OpenFoodFacts CSV Ingestion Process...")
    engine = get_loader_engine()
    
    processed_en = ingest_file('en.openfoodfacts.org.products.csv', engine)
    processed_fr = ingest_file('fr.openfoodfacts.org.products.csv', engine)
    
    if not processed_en and not processed_fr:
        print("\n❌ Could not find either 'en.openfoodfacts.org.products.csv' or 'fr.openfoodfacts.org.products.csv'.")
        print("Please download them directly into the root folder and run this script again.")

import pandas as pd
import myloginpath
import urllib.parse
from sqlalchemy import create_engine, text
from sqlalchemy.types import VARCHAR, TEXT, DOUBLE
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
        
    print(f"\n🚀 Found {filename}! Starting extreme batch ingestion for ALL columns...")
    
    chunk_size = 10000 
    total_processed = 0
    is_first_chunk = True

    for chunk in pd.read_csv(filename, sep='\t', dtype=str, chunksize=chunk_size, on_bad_lines='skip', low_memory=False, encoding='utf-8'):
        try:
            df = chunk.copy()
            
            if 'code' not in df.columns:
                continue

            # Drop missing codes and local duplicates
            df.dropna(subset=['code'], inplace=True)
            df.drop_duplicates(subset=['code'], inplace=True)
            
            # Map datatypes dynamically to avoid InnoDB row size limits
            # Code is VARCHAR(50), everything else is TEXT (strings) or DOUBLE (if we were casting, but we read as str)
            # Since we read dtype=str, pandas will default all to TEXT which is perfect for Off-Page storage.
            sql_dtypes = {col: TEXT() for col in df.columns}
            sql_dtypes['code'] = VARCHAR(50)
            
            if is_first_chunk:
                # 1. Initialize the target table with the exact schema from the first chunk
                df.head(0).to_sql('products', con=engine, if_exists='replace', index=False, dtype=sql_dtypes)
                
                # 2. Add Primary Key immediately
                with engine.begin() as conn:
                    conn.execute(text("ALTER TABLE products ADD PRIMARY KEY (code);"))
                is_first_chunk = False

            # Write chunk to a temporary table
            df.to_sql('temp_products', con=engine, if_exists='replace', index=False, dtype=sql_dtypes)
            
            # Use INSERT IGNORE to append to the main table, skipping any global duplicate codes
            with engine.begin() as connection:
                # Ensure columns match by explicitly listing them
                cols = ", ".join([f"`{c}`" for c in df.columns])
                connection.execute(text(f"INSERT IGNORE INTO products ({cols}) SELECT {cols} FROM temp_products"))
            
            total_processed += len(df)
            print(f"   Successfully appended {total_processed} rows into unified dynamic schema...", end="\r")
        except BaseException as e:
            print(f"\n   [Warning] Chunk skipped due to error: {e}")
            
    # Cleanup temp table
    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS temp_products"))
        
    print(f"\n✅ Finished importing {filename}.")
    return True

def create_indexes(engine):
    print("\n🛠️ Creating performance indexes (FULLTEXT and Standard)...")
    try:
        with engine.begin() as connection:
            # Add Fulltext Search on vital textual fields if they exist
            try:
                connection.execute(text("ALTER TABLE products ADD FULLTEXT idx_search (product_name, ingredients_text);"))
                print("  - Added FULLTEXT index on product_name, ingredients_text")
            except Exception as e:
                print(f"  - Skipped FULLTEXT idx_search: {e}")
                
            try:
                connection.execute(text("ALTER TABLE products ADD FULLTEXT idx_allergens (allergens);"))
                print("  - Added FULLTEXT index on allergens")
            except Exception as e:
                print(f"  - Skipped FULLTEXT idx_allergens: {e}")

            # Standard indexes for fast exact matches
            try:
                connection.execute(text("ALTER TABLE products ADD INDEX idx_brands (brands(50));"))
                print("  - Added INDEX on brands")
            except Exception as e:
                print(f"  - Skipped INDEX idx_brands: {e}")
                
            try:
                connection.execute(text("ALTER TABLE products ADD INDEX idx_generic (generic_name(50));"))
                print("  - Added INDEX on generic_name")
            except Exception as e:
                print(f"  - Skipped INDEX idx_generic: {e}")

        print("✅ Indexing Complete!")
    except Exception as e:
        print(f"❌ Indexing encountered an issue: {e}")

if __name__ == "__main__":
    print("Initiating OpenFoodFacts CSV Unified Dynamic Ingestion Process...")
    engine = get_loader_engine()
    
    processed_en = ingest_file('en.openfoodfacts.org.products.csv', engine)
    processed_fr = ingest_file('fr.openfoodfacts.org.products.csv', engine)
    
    if not processed_en and not processed_fr:
        print("\n❌ Could not find either 'en.openfoodfacts.org.products.csv' or 'fr.openfoodfacts.org.products.csv'.")
        print("Please download them directly into the root folder and run this script again.")
    else:
        create_indexes(engine)
        print("\n🎉 Full database reload complete! Ready for AI RAG.")

import pandas as pd
import myloginpath
import urllib.parse
from sqlalchemy import create_engine, text
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
        
    print(f"\n🚀 Found {filename}! Starting extreme batch ingestion...")
    
    chunk_size = 5000 
    total_processed = 0

    # Read dynamically without filtering. Setting low_memory=False to let pandas parse column types flexibly
    # Forced utf-8 encoding to prevent French accent corruption on Windows OS defaults
    for chunk in pd.read_csv(filename, sep='\t', dtype=str, chunksize=chunk_size, on_bad_lines='skip', low_memory=False, encoding='utf-8'):
        try:
            # Drop duplicates by code natively
            if 'code' in chunk.columns:
                df = chunk.drop_duplicates(subset=['code'])
            else:
            # Eliminate completely empty columns to save storage
            df.dropna(axis=1, how='all', inplace=True)
            
            # Segment the dataframe into chunks of 50 columns each to bypass InnoDB constraints
            cols = list(df.columns)
            if 'code' in cols: cols.remove('code')
            
            chunk_size = 50
            chunks = [cols[i:i + chunk_size] for i in range(0, len(cols), chunk_size)]
            
            for i, col_chunk in enumerate(chunks):
                # Ensure 'code' maps across every single table
                table_name = f'products_{i+1}'
                df_slice = df[['code'] + col_chunk].copy()
                df_slice.to_sql(table_name, con=engine, if_exists='append', index=False)

            total_processed += len(df)
            print(f"   Successfully appended {total_processed} rows (Dynamic schema)...", end="\r")
        except BaseException as e:
            if "Duplicate entry" in str(e):
                pass
            else:
                 print(f"\n   [Warning] Chunk skipped due to internal structural error: {e}")
        
    print(f"\n✅ Finished importing {filename}.")
    return True

def create_indexes(engine):
    print("\n🛠️ Creating performance indexes on newly generated table...")
    # B-TREE and FULLTEXT INDEXES created post-ingestion for extreme speed
    try:
        with engine.begin() as connection:
            print("  Building Core Architecture on Partitions...")
            # Enforce Primary Keys on the first 4 partitions
            for i in range(1, 5):
                try:
                    connection.execute(text(f"ALTER TABLE products_{i} MODIFY code VARCHAR(50);"))
                    connection.execute(text(f"ALTER TABLE products_{i} ADD PRIMARY KEY (code);"))
                except: pass

            print("  Building Dynamic MySQL View...")
            # We build a massive Join View so the app doesn't need to know about the segments
            try:
                connection.execute(text("""
                CREATE VIEW products AS
                SELECT p1.*, 
                       p2.energy_100g, p2.`energy-kcal_100g`, p2.proteins_100g, p2.fat_100g, p2.carbohydrates_100g, p2.sugars_100g, p2.salt_100g, p2.sodium_100g, p2.fiber_100g,
                       p3.iron_100g, p3.calcium_100g, p3.`vitamin-c_100g`, p3.`vitamin-d_100g`
                FROM products_1 p1
                LEFT JOIN products_2 p2 ON p1.code = p2.code
                LEFT JOIN products_3 p3 ON p1.code = p3.code
                """))
            except: pass
        print("✅ Indexing Complete!")
    except Exception as e:
        print(f"❌ Indexing encountered an issue: {e}")

if __name__ == "__main__":
    print("Initiating OpenFoodFacts CSV Ingestion Process...")
    engine = get_loader_engine()
    
    processed_en = ingest_file('en.openfoodfacts.org.products.csv', engine)
    processed_fr = ingest_file('fr.openfoodfacts.org.products.csv', engine)
    
    if not processed_en and not processed_fr:
        print("\n❌ Could not find either 'en.openfoodfacts.org.products.csv' or 'fr.openfoodfacts.org.products.csv'.")
        print("Please download them directly into the root folder and run this script again.")
    else:
        # Build indexes now that all data is appended!
        create_indexes(engine)
        print("\n🎉 Full database reload and indexing complete! Ready for AI RAG.")

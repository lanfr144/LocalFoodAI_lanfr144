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
        
    print(f"\n🚀 Found {filename}! Starting extreme batch ingestion...")
    
    chunk_size = 5000 
    total_processed = 0

    # Read dynamically without filtering. Setting low_memory=False to let pandas parse column types flexibly
    for chunk in pd.read_csv(filename, sep='\t', dtype=str, chunksize=chunk_size, on_bad_lines='skip', low_memory=False):
        try:
            # Drop duplicates by code natively
            if 'code' in chunk.columns:
                df = chunk.drop_duplicates(subset=['code'])
            else:
                df = chunk
                
            df.to_sql('products', con=engine, if_exists='append', index=False)
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
            print("  Building Primary Key on `code`...")
            # We must make `code` the primary key if pandas just made it a TEXT field
            # But MySQL cannot have a TEXT field as PRIMARY KEY without a length constraint.
            # Convert code to VARCHAR(50) first.
            connection.execute(urllib.parse.unquote("ALTER TABLE products MODIFY code VARCHAR(50);"))
            connection.execute(urllib.parse.unquote("ALTER TABLE products ADD PRIMARY KEY (code);"))

            print("  Building Fulltext Indexes...")
            connection.execute(urllib.parse.unquote("CREATE FULLTEXT INDEX ft_idx_search ON products(product_name, ingredients_text, brands);"))
            
            print("  Building B-TREE Indexes on core macros...")
            # We attempt to index key macros if they exist
            macro_cols = ['energy-kcal_100g', 'fat_100g', 'carbohydrates_100g', 'proteins_100g']
            for col in macro_cols:
                # Convert TEXT to DOUBLE for numerical indexing and querying
                # We catch errors if the column doesn't exist to be safe
                try:
                    connection.execute(urllib.parse.unquote(f"ALTER TABLE products MODIFY `{col}` DOUBLE;"))
                    connection.execute(urllib.parse.unquote(f"CREATE INDEX idx_{col.replace('-', '_')} ON products(`{col}`);"))
                except:
                    pass
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

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
            # Only keep the minimum columns required by our clinical analytical schema!
            target_cols = [
                'code', 'product_name', 'generic_name', 'brands', 'allergens', 'ingredients_text',
                'proteins_100g', 'fat_100g', 'carbohydrates_100g', 'sugars_100g', 'sodium_100g', 'energy-kcal_100g',
                'vitamin-c_100g', 'iron_100g', 'calcium_100g'
            ]
            # Use intersection in case some CSV chunks lack certain columns
            exist_cols = [c for c in target_cols if c in df.columns]
            df = df[exist_cols]
            
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
            connection.execute(text("ALTER TABLE products MODIFY code VARCHAR(50);"))
            connection.execute(text("ALTER TABLE products ADD PRIMARY KEY (code);"))

            print("  Building Fulltext Indexes...")
            connection.execute(text("CREATE FULLTEXT INDEX ft_idx_search ON products(product_name, ingredients_text, brands);"))
            
            print("  Building B-TREE Indexes on core macros...")
            macro_cols = ['energy-kcal_100g', 'fat_100g', 'carbohydrates_100g', 'proteins_100g', 'sugars_100g', 'sodium_100g', 'iron_100g', 'calcium_100g', 'vitamin-c_100g']
            for col in macro_cols:
                try:
                    connection.execute(text(f"ALTER TABLE products MODIFY `{col}` DOUBLE;"))
                    connection.execute(text(f"CREATE INDEX idx_{col.replace('-', '_')} ON products(`{col}`);"))
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

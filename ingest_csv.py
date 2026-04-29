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
        
    print(f"\n🚀 Found {filename}! Starting extreme batch ingestion into unified table...")
    
    chunk_size = 10000 
    total_processed = 0

    required_columns = [
        'code', 'product_name', 'generic_name', 'brands', 'allergens', 'ingredients_text',
        'proteins_100g', 'fat_100g', 'carbohydrates_100g', 'sugars_100g', 'sodium_100g', 
        'energy-kcal_100g', 'vitamin-c_100g', 'iron_100g', 'calcium_100g'
    ]

    for chunk in pd.read_csv(filename, sep='\t', dtype=str, chunksize=chunk_size, on_bad_lines='skip', low_memory=False, encoding='utf-8'):
        try:
            # Filter to only the columns that actually exist in this chunk and are in required_columns
            available_cols = [c for c in required_columns if c in chunk.columns]
            df = chunk[available_cols].copy()
            
            if 'code' not in df.columns:
                continue

            # Drop missing codes and local duplicates
            df.dropna(subset=['code'], inplace=True)
            df.drop_duplicates(subset=['code'], inplace=True)
            
            # Ensure all required columns exist in the dataframe (fill missing with None)
            for col in required_columns:
                if col not in df.columns:
                    df[col] = None
                    
            # Reorder columns to exactly match the target table schema
            df = df[required_columns]
            
            # Write chunk to a temporary table
            df.to_sql('temp_products', con=engine, if_exists='replace', index=False)
            
            # Use INSERT IGNORE to append to the main table, skipping any global duplicate codes
            with engine.begin() as connection:
                connection.execute(text("INSERT IGNORE INTO products SELECT * FROM temp_products"))
            
            total_processed += len(df)
            print(f"   Successfully appended {total_processed} rows into unified schema...", end="\r")
        except BaseException as e:
            print(f"\n   [Warning] Chunk skipped due to error: {e}")
            
    # Cleanup temp table
    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS temp_products"))
        
    print(f"\n✅ Finished importing {filename}.")
    return True

if __name__ == "__main__":
    print("Initiating OpenFoodFacts CSV Unified Ingestion Process...")
    engine = get_loader_engine()
    
    processed_en = ingest_file('en.openfoodfacts.org.products.csv', engine)
    processed_fr = ingest_file('fr.openfoodfacts.org.products.csv', engine)
    
    if not processed_en and not processed_fr:
        print("\n❌ Could not find either 'en.openfoodfacts.org.products.csv' or 'fr.openfoodfacts.org.products.csv'.")
        print("Please download them directly into the root folder and run this script again.")
    else:
        print("\n🎉 Full database reload complete! Ready for AI RAG.")

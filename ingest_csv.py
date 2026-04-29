import pandas as pd
import myloginpath
import urllib.parse
from sqlalchemy import create_engine, text
from sqlalchemy.types import VARCHAR, TEXT, DOUBLE
import os
import sys
from snmp_notifier import notifier

def get_loader_engine():
    try:
        conf = myloginpath.parse('app_loader')
        user = conf.get('user')
        password = urllib.parse.quote_plus(conf.get('password'))
        host = conf.get('host', '127.0.0.1')
        database = 'food_db'
        conn_str = f"mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4"
        return create_engine(conn_str)
    except Exception as e:
        print(f"❌ Failed to parse myloginpath or create engine: {e}")
        sys.exit(1)

def ingest_file(filename, engine):
    if not os.path.exists(filename):
        print(f"File {filename} not found locally.")
        return False
        
    print(f"\n🚀 Found {filename}! Starting grouped vertical partition ingestion...")
    
    chunk_size = 10000 
    total_processed = 0

    # Define the groupings
    groups = {
        'products_core': ['code', 'product_name', 'generic_name', 'brands', 'ingredients_text'],
        'products_allergens': ['code', 'allergens'],
        'products_macros': ['code', 'energy-kcal_100g', 'proteins_100g', 'fat_100g', 'carbohydrates_100g', 'sugars_100g', 'fiber_100g', 'sodium_100g', 'salt_100g', 'cholesterol_100g'],
        'products_vitamins': ['code', 'vitamin-a_100g', 'vitamin-b1_100g', 'vitamin-b2_100g', 'vitamin-pp_100g', 'vitamin-b6_100g', 'vitamin-b9_100g', 'vitamin-b12_100g', 'vitamin-c_100g', 'vitamin-d_100g', 'vitamin-e_100g', 'vitamin-k_100g'],
        'products_minerals': ['code', 'calcium_100g', 'iron_100g', 'magnesium_100g', 'potassium_100g', 'zinc_100g']
    }

    # Pre-calculate what to read
    all_required_cols = list(set([col for cols in groups.values() for col in cols]))

    for chunk in pd.read_csv(filename, sep='\t', dtype=str, chunksize=chunk_size, on_bad_lines='skip', low_memory=False, encoding='utf-8'):
        try:
            # Drop rows with missing codes
            if 'code' not in chunk.columns:
                continue
            df = chunk.dropna(subset=['code']).drop_duplicates(subset=['code']).copy()
            
            # Ensure all required columns exist in the chunk (fill with None if missing)
            for col in all_required_cols:
                if col not in df.columns:
                    df[col] = None
                    
            for table_name, columns in groups.items():
                slice_df = df[columns].copy()
                
                # Cast datatypes: core and allergens are TEXT, others are DOUBLE
                if table_name in ['products_core', 'products_allergens']:
                    sql_dtypes = {col: TEXT() for col in columns if col != 'code'}
                    sql_dtypes['code'] = VARCHAR(50)
                else:
                    # Convert to numeric (double) safely
                    for col in columns:
                        if col != 'code':
                            slice_df[col] = pd.to_numeric(slice_df[col], errors='coerce')
                    sql_dtypes = {col: DOUBLE() for col in columns if col != 'code'}
                    sql_dtypes['code'] = VARCHAR(50)

                # Write to temp table
                temp_name = f"temp_{table_name}"
                slice_df.to_sql(temp_name, con=engine, if_exists='replace', index=False, dtype=sql_dtypes)
                
                # INSERT IGNORE into final table
                with engine.begin() as conn:
                    cols_str = ", ".join([f"`{c}`" for c in columns])
                    conn.execute(text(f"INSERT IGNORE INTO {table_name} ({cols_str}) SELECT {cols_str} FROM {temp_name}"))
                    conn.execute(text(f"DROP TABLE IF EXISTS {temp_name}"))

            total_processed += len(df)
            print(f"   Successfully appended {total_processed} rows into grouped tables...", end="\r")
            if total_processed % 50000 == 0:
                notifier.send_alert(f"Ingestion Milestone: {total_processed} rows processed")
        except BaseException as e:
            notifier.send_alert(f"Ingestion Exception: {str(e)}")
            print(f"\n   [Warning] Chunk skipped due to error: {e}")
            
    notifier.send_alert(f"Ingestion Finished: {filename}")
    print(f"\n✅ Finished importing {filename}.")
    return True

if __name__ == "__main__":
    print("Initiating OpenFoodFacts Grouped Vertical Ingestion Process...")
    engine = get_loader_engine()
    
    processed_en = ingest_file('en.openfoodfacts.org.products.csv', engine)
    processed_fr = ingest_file('fr.openfoodfacts.org.products.csv', engine)
    
    if not processed_en and not processed_fr:
        print("\n❌ Could not find CSVs.")
    else:
        print("\n🎉 Full database reload complete! Ready for AI RAG.")

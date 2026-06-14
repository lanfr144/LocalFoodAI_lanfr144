#!/usr/bin/env python3
#ident "@(#)$Format:LocalFoodAI:ingest_csv.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import pandas as pd
import myloginpath
import urllib.parse
from sqlalchemy import create_engine, text
from sqlalchemy.types import VARCHAR, DOUBLE
from sqlalchemy.dialects.mysql import LONGTEXT
import os
import sys
from snmp_notifier import notifier

def get_loader_engine():
    try:
        import os
        db_host = os.environ.get('DB_HOST')
        db_user = os.environ.get('DB_USER')
        db_pass = os.environ.get('DB_PASS')

        if db_host and db_user and db_pass:
            password = urllib.parse.quote_plus(db_pass)
            conn_str = f"mysql+pymysql://{db_user}:{password}@{db_host}/food_db?charset=utf8mb4"
            return create_engine(conn_str)
            
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

def init_ingestion_status_table(engine):
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ingestion_status (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255),
                start_time DATETIME,
                end_time DATETIME,
                rows_loaded INT,
                status VARCHAR(50),
                error_message TEXT
            )
        """))

def ingest_file(filename, engine):
    if not os.path.exists(filename):
        print(f"File {filename} not found locally.")
        return False
        
    print(f"\n🚀 Found {filename}! Starting grouped vertical partition ingestion...")
    
    chunk_size = 10000 
    total_processed = 0
    max_chunks = int(os.environ.get('MAX_CHUNKS', '0'))
    chunks_count = 0

    # Define the groupings
    groups = {
        'products_core': [
            'code', 'product_name', 'generic_name', 'brands', 'ingredients_text',
            'url', 'image_url', 'image_small_url', 'image_ingredients_url', 
            'image_ingredients_small_url', 'image_nutrition_url', 'image_nutrition_small_url'
        ],
        'products_allergens': ['code', 'allergens'],
        'products_macros': ['code', 'energy-kcal_100g', 'proteins_100g', 'fat_100g', 'carbohydrates_100g', 'sugars_100g', 'fiber_100g', 'sodium_100g', 'salt_100g', 'cholesterol_100g'],
        'products_vitamins': ['code', 'vitamin-a_100g', 'vitamin-b1_100g', 'vitamin-b2_100g', 'vitamin-pp_100g', 'vitamin-b6_100g', 'vitamin-b9_100g', 'vitamin-b12_100g', 'vitamin-c_100g', 'vitamin-d_100g', 'vitamin-e_100g', 'vitamin-k_100g'],
        'products_minerals': ['code', 'calcium_100g', 'iron_100g', 'magnesium_100g', 'potassium_100g', 'zinc_100g']
    }

    # Schema Auto-Migration: check if columns mismatch, and drop table for clean recreation
    try:
        with engine.connect() as conn:
            for table_name, columns in groups.items():
                try:
                    res = conn.execute(text(f"DESCRIBE {table_name}"))
                    existing_cols = [row[0] for row in res.fetchall()]
                    mismatch = False
                    for col in columns:
                        if col not in existing_cols:
                            mismatch = True
                            break
                    if mismatch:
                        print(f"⚠️ Columns mismatch for table {table_name}. Dropping table for recreation.")
                        conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
                        conn.commit()
                except Exception:
                    pass
    except Exception as e:
        print(f"Warning: Could not connect to database for schema check: {e}")

    # Pre-calculate what to read
    all_required_cols = list(set([col for cols in groups.values() for col in cols]))

    for chunk in pd.read_csv(filename, sep='\t', dtype=str, chunksize=chunk_size, on_bad_lines='skip', low_memory=False, encoding='utf-8'):
        chunks_count += 1
        if max_chunks > 0 and chunks_count > max_chunks:
            print(f"\nReached MAX_CHUNKS limit ({max_chunks}). Ingestion stopped early.")
            break
        try:
            # Drop rows with missing codes
            if 'code' not in chunk.columns:
                continue
            df = chunk.dropna(subset=['code']).drop_duplicates(subset=['code']).copy()
            
            # Clean and consolidate CSV data
            # 1. Clean code (must be numeric digits/characters, strip whitespace)
            df['code'] = df['code'].astype(str).str.strip()
            df = df[df['code'] != '']
            
            # 2. Clean product_name: strip whitespace, fill empty with generic name or brand, or skip if completely empty
            if 'product_name' in df.columns:
                df['product_name'] = df['product_name'].astype(str).str.strip()
                if 'generic_name' in df.columns:
                    df['product_name'] = df['product_name'].fillna(df['generic_name'].astype(str).str.strip())
                if 'brands' in df.columns:
                    df['product_name'] = df['product_name'].fillna(df['brands'].astype(str).str.strip())
                # Replace string representations of "nan" / "none"
                df['product_name'] = df['product_name'].replace(['nan', 'NaN', 'None', 'none', ''], None)
                
            # 3. Drop rows with missing or null product_name (consolidate only valid food items)
            df = df.dropna(subset=['product_name'])
            
            # 4. Clean URL columns: if not starts with http/https or contains 'invalid', set to None
            url_cols = [c for c in df.columns if 'url' in c.lower()]
            for col in url_cols:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace(['nan', 'NaN', 'None', 'none', ''], None)
                # Validate URL structure
                is_valid_url = df[col].str.startswith(('http://', 'https://'), na=False) & ~df[col].str.contains('invalid', case=False, na=False)
                df.loc[~is_valid_url, col] = None
            
            # Ensure all required columns exist in the chunk (fill with None if missing)
            for col in all_required_cols:
                if col not in df.columns:
                    df[col] = None
                    
            for table_name, columns in groups.items():
                slice_df = df[columns].copy()
                
                # Cast datatypes: core and allergens are TEXT, others are DOUBLE
                if table_name in ['products_core', 'products_allergens']:
                    sql_dtypes = {col: LONGTEXT() for col in columns if col != 'code'}
                    sql_dtypes['code'] = VARCHAR(255)
                else:
                    # Convert to numeric (double) safely
                    for col in columns:
                        if col != 'code':
                            slice_df[col] = pd.to_numeric(slice_df[col], errors='coerce')
                    sql_dtypes = {col: DOUBLE() for col in columns if col != 'code'}
                    sql_dtypes['code'] = VARCHAR(255)

                # Write to temp table
                temp_name = f"temp_{table_name}"
                slice_df.to_sql(temp_name, con=engine, if_exists='replace', index=False, dtype=sql_dtypes)
                
                # UPSERT into final table with Primary Key enforcement
                with engine.begin() as conn:
                    # Ensure temp table has a primary key on code so LIKE copies it, or alter it later
                    conn.execute(text(f"ALTER TABLE {temp_name} ADD PRIMARY KEY (code);"))
                    conn.execute(text(f"CREATE TABLE IF NOT EXISTS {table_name} LIKE {temp_name}"))
                    
                    cols_str = ", ".join([f"`{c}`" for c in columns])
                    # Generate ON DUPLICATE KEY UPDATE clause with COALESCE to fill nulls
                    update_cols = ", ".join([f"`{c}` = COALESCE(`{table_name}`.`{c}`, VALUES(`{c}`))" for c in columns if c != 'code'])
                    
                    if update_cols:
                        upsert_query = f"INSERT INTO {table_name} ({cols_str}) SELECT {cols_str} FROM {temp_name} ON DUPLICATE KEY UPDATE {update_cols}"
                    else:
                        upsert_query = f"INSERT IGNORE INTO {table_name} ({cols_str}) SELECT {cols_str} FROM {temp_name}"
                        
                    conn.execute(text(upsert_query))
                    conn.execute(text(f"DROP TABLE IF EXISTS {temp_name}"))

            total_processed += len(df)
            print(f"   Successfully appended {total_processed} rows into grouped tables...", end="\r")
            
            # Update rows loaded in database
            with engine.begin() as conn:
                conn.execute(text("""
                    UPDATE ingestion_status 
                    SET rows_loaded = :rows
                    WHERE id = :id
                """), {"rows": total_processed, "id": ingest_id})
                
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
    
    processed_en = ingest_file('data/en.openfoodfacts.org.products.csv', engine)
    processed_fr = ingest_file('data/fr.openfoodfacts.org.products.csv', engine)
    
    if not processed_en and not processed_fr:
        print("\n❌ Could not find CSVs.")
    else:
        print("\n🎉 Full database reload complete! Ready for AI RAG.")
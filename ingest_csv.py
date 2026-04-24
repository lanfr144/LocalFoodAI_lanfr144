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
                df = chunk
            # Eliminate completely empty columns to save storage
            df.dropna(axis=1, how='all', inplace=True)
            
            # Segment the dataframe into chunks of 50 columns each to bypass InnoDB constraints
            cols = list(df.columns)
            if 'code' in cols: cols.remove('code')
            
            p_chunk_size = 8 # Safe size for TEXT columns
            chunks = [cols[i:i + p_chunk_size] for i in range(0, len(cols), p_chunk_size)]
            
            for i, col_chunk in enumerate(chunks):
                table_name = f'products_{i+1}'
                df_slice = df[['code'] + col_chunk].copy()
                df_slice.to_sql(table_name, con=engine, if_exists='append', index=False)

            total_processed += len(df)
            print(f"   Successfully appended {total_processed} rows (Dynamic schema)...", end="\r")
        except BaseException as e:
            if "Duplicate entry" in str(e):
                pass
            else:
                 print(f"\n   [Warning] Chunk skipped due to error: {e}")
        
    print(f"\n✅ Finished importing {filename}.")
    return True

def create_indexes(engine):
    # Determine how many tables were actually created
    num_tables = 0
    with engine.connect() as conn:
        res = conn.execute(text("SHOW TABLES LIKE 'products_%'"))
        num_tables = len(res.fetchall())

    print(f"\n🛠️ Creating performance indexes on {num_tables} partition tables...")
    try:
        with engine.begin() as connection:
            # Enforce Primary Keys on ALL partitions
            for i in range(1, num_tables + 1):
                try:
                    connection.execute(text(f"ALTER TABLE products_{i} MODIFY code VARCHAR(50);"))
                    connection.execute(text(f"ALTER TABLE products_{i} ADD PRIMARY KEY (code);"))
                except: pass

            print("  Building Global MySQL VIEW...")
            view_sql = f"CREATE VIEW products AS SELECT p1.* "
            joins = []
            for i in range(2, num_tables + 1):
                # Get columns for this table except 'code'
                cols_res = connection.execute(text(f"SHOW COLUMNS FROM products_{i}"))
                table_cols = [c[0] for c in cols_res.fetchall() if c[0] != 'code']
                if table_cols:
                    view_sql += ", " + ", ".join([f"p{i}.`{c}`" for c in table_cols])
                joins.append(f"LEFT JOIN products_{i} p{i} ON p1.code = p{i}.code")
            
            view_sql += " FROM products_1 p1 " + " ".join(joins)
            
            try:
                connection.execute(text(view_sql))
            except Exception as ev:
                print(f"  Warning: View creation failed: {ev}")
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

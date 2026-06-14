import re
import os

file_path = "ingest_csv.py"
with open(file_path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# Replace encoding issues in header
content = content.replace("Lange FranA ois", "Francois Lange")
content = content.replace("Lange FranAois", "Francois Lange")
content = content.replace("Lange François", "Francois Lange")

# 1. Add init_ingestion_status_table function definition right before ingest_file
old_def = "def ingest_file(filename, engine):"
new_def = """def init_ingestion_status_table(engine):
    with engine.begin() as conn:
        conn.execute(text(\"\"\"
            CREATE TABLE IF NOT EXISTS ingestion_status (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename VARCHAR(255),
                start_time DATETIME,
                end_time DATETIME,
                rows_loaded INT,
                status VARCHAR(50),
                error_message TEXT
            )
        \"\"\"))

def ingest_file(filename, engine):"""

content = content.replace(old_def, new_def)

# 2. Add table initialization and insert running status in ingest_file
old_start = """    print(f"\\ndYs? Found {filename}! Starting grouped vertical partition ingestion...")
    
    chunk_size = 10000 
    total_processed = 0"""

new_start = """    print(f"\\ndYs? Found {filename}! Starting grouped vertical partition ingestion...")
    
    # Initialize ingestion status tracking
    init_ingestion_status_table(engine)
    import datetime
    start_time = datetime.datetime.now()
    
    with engine.begin() as conn:
        conn.execute(text(\"\"\"
            INSERT INTO ingestion_status (filename, start_time, rows_loaded, status)
            VALUES (:filename, :start_time, 0, 'RUNNING')
        \"\"\"), {"filename": filename, "start_time": start_time})
        last_id_res = conn.execute(text("SELECT LAST_INSERT_ID()"))
        ingest_id = last_id_res.scalar()

    chunk_size = 10000 
    total_processed = 0"""

content = content.replace(old_start, new_start)

# 3. Add milestone updates inside chunk loop
old_milestone = """            total_processed += len(df)
            print(f"   Successfully appended {total_processed} rows into grouped tables...", end="\\r")
            if total_processed % 50000 == 0:
                notifier.send_alert(f"Ingestion Milestone: {total_processed} rows processed")"""

new_milestone = """            total_processed += len(df)
            print(f"   Successfully appended {total_processed} rows into grouped tables...", end="\\r")
            
            # Update rows loaded in database
            with engine.begin() as conn:
                conn.execute(text(\"\"\"
                    UPDATE ingestion_status 
                    SET rows_loaded = :rows
                    WHERE id = :id
                \"\"\"), {"rows": total_processed, "id": ingest_id})
                
            if total_processed % 50000 == 0:
                notifier.send_alert(f"Ingestion Milestone: {total_processed} rows processed")"""

content = content.replace(old_milestone, new_milestone)

# 4. Add success and failure callbacks at the end
old_end = """        except BaseException as e:
            notifier.send_alert(f"Ingestion Exception: {str(e)}")
            print(f"\\n   [Warning] Chunk skipped due to error: {e}")
            
    notifier.send_alert(f"Ingestion Finished: {filename}")
    print(f"\\no. Finished importing {filename}.")
    return True"""

new_end = """        except BaseException as e:
            end_time = datetime.datetime.now()
            with engine.begin() as conn:
                conn.execute(text(\"\"\"
                    UPDATE ingestion_status 
                    SET end_time = :end_time, status = 'FAILED', error_message = :err
                    WHERE id = :id
                \"\"\"), {"end_time": end_time, "err": str(e), "id": ingest_id})
            notifier.send_alert(f"Ingestion Exception: {str(e)}")
            print(f"\\n   [Warning] Chunk skipped due to error: {e}")
            
    end_time = datetime.datetime.now()
    with engine.begin() as conn:
        conn.execute(text(\"\"\"
            UPDATE ingestion_status 
            SET end_time = :end_time, status = 'COMPLETED'
            WHERE id = :id
        \"\"\"), {"end_time": end_time, "id": ingest_id})
        
    notifier.send_alert(f"Ingestion Finished: {filename}")
    print(f"\\n. Finished importing {filename}.")
    return True"""

content = content.replace(old_end, new_end)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("ingest_csv.py successfully updated.")

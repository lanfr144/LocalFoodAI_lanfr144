#!/usr/bin/env python3
#ident "@(#)$Format:LocalFoodAI:zabbix_telemetry.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$""
import os
import sys
import pymysql
from dotenv import load_dotenv

def get_db_connection():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(current_dir, '.env')
    load_dotenv(dotenv_path=env_path)
    
    # Try environment variables from compose or env
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_user = os.environ.get('DB_USER') or os.environ.get('DB_LOADER_USER') or 'food_loader'
    db_pass = os.environ.get('DB_PASS') or os.environ.get('DB_LOADER_PASS') or 'BTSai123'
    
    # Check if .env config parameters exist
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip().startswith('MYSQL_ROOT_PASSWORD'):
                    db_pass = line.split('=')[1].strip()
                    db_user = 'root'
                elif line.strip().startswith('DB_LOADER_PASS') and db_user != 'root':
                    db_pass = line.split('=')[1].strip()
                    db_user = 'food_loader'
                    
    # Shifted MySQL Port check (if WSL or local offset)
    db_port = 3306
    if os.environ.get('NETWORK_MODE') == 'local' or os.path.exists(os.path.join(current_dir, 'docker-compose-wsl.yml')):
        db_port = 3326
        
    return pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database='food_db',
        port=db_port,
        cursorclass=pymysql.cursors.DictCursor
    )

def main():
    if len(sys.argv) < 2:
        print("Usage: python zabbix_telemetry.py [status|rows|start|end]")
        sys.exit(1)
        
    metric = sys.argv[1].lower()
    
    try:
        conn = get_db_connection()
    except Exception as e:
        if metric == 'status':
            print("OFFLINE")
        elif metric == 'rows':
            print("0")
        else:
            print("N/A")
        sys.exit(0)
        
    try:
        with conn.cursor() as cursor:
            # Query the last ingestion run details
            cursor.execute("""
                SELECT status, start_time, end_time, rows_loaded 
                FROM ingestion_status 
                ORDER BY id DESC LIMIT 1
            """)
            row = cursor.fetchone()
            
            if not row:
                if metric == 'status': print("NO_DATA")
                elif metric == 'rows': print("0")
                else: print("N/A")
                sys.exit(0)
                
            if metric == 'status':
                print(row['status'])
            elif metric == 'rows':
                print(row['rows_loaded'])
            elif metric == 'start':
                print(row['start_time'].strftime("%Y-%m-%d %H:%M:%S") if row['start_time'] else "N/A")
            elif metric == 'end':
                print(row['end_time'].strftime("%Y-%m-%d %H:%M:%S") if row['end_time'] else "N/A")
            else:
                print("INVALID_METRIC")
    except Exception as e:
        if metric == 'status': print("ERROR")
        elif metric == 'rows': print("-1")
        else: print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
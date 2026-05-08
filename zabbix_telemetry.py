import os
import time
from app import get_db_connection
from snmp_notifier import notifier

def report_telemetry():
    conn = get_db_connection('app_reader')
    if not conn:
        print("Failed to connect to database for telemetry.")
        return
    
    try:
        with conn.cursor() as cursor:
            # Get products count
            cursor.execute("SELECT COUNT(*) as cnt FROM food_db.products_core")
            products_count = cursor.fetchone()['cnt']
            
            # Get users count
            cursor.execute("SELECT COUNT(*) as cnt FROM food_db.users")
            users_count = cursor.fetchone()['cnt']
            
            msg = f"TELEMETRY: products_core_count={products_count}, users_count={users_count}"
            print(f"Sending to Zabbix: {msg}")
            
            # Push via SNMP Trap (which is hooked into Zabbix server on 192.168.130.170)
            notifier.send_alert(msg)
            
    except Exception as e:
        print(f"Telemetry error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    report_telemetry()

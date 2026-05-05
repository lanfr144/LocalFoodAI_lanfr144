import os
import socket

class SNMPNotifier:
    def __init__(self, target_host='192.168.130.170', target_port=162):
        self.target_host = target_host
        self.target_port = target_port
        self.user = 'zabbix_snmp'
        self.auth_key = 'authkey123'
        self.priv_key = 'privkey123'

    def send_alert(self, message):
        try:
            # Using the standard snmptrap CLI which is more stable than pysnmp v7
            hostname = socket.gethostname()
            safe_message = str(message).replace("'", "").replace('"', '')
            cmd = f"snmptrap -v3 -l authPriv -u {self.user} -a SHA -A {self.auth_key} -x AES -X {self.priv_key} {self.target_host}:{self.target_port} '' 1.3.6.1.4.1.8072.3.2.10 1.3.6.1.2.1.1.1.0 s '[{hostname}] {safe_message}'"
            os.system(cmd)
        except Exception as e:
            print(f"Failed to send SNMPv3 trap: {e}")

# Singleton instance
notifier = SNMPNotifier()


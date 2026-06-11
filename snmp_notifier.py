#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os
import socket
#ident "@(#)$Format:LocalFoodAI:snmp_notifier.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import socket

class SNMPNotifier:
    def __init__(self, target_host=None, target_port=162):
        self.target_host = target_host or os.environ.get('ZABBIX_HOST', '192.168.130.170')
        self.target_port = target_port
        self.user = os.environ.get('ZABBIX_SNMP_USER', '')
        self.auth_key = os.environ.get('ZABBIX_SNMP_AUTHKEY', '')
        self.priv_key = os.environ.get('ZABBIX_SNMP_PRIVKEY', '')

    def send_alert(self, message):
        if os.environ.get('NETWORK_MODE', 'server') == 'local':
            print(f"[OFFLINE MODE] Suppressed SNMP trap: {message}")
            return
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

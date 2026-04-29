import time
import socket
from pysnmp.hlapi import *

class SNMPNotifier:
    def __init__(self, target_host='192.168.130.170', target_port=162):
        self.target_host = target_host
        self.target_port = target_port
        self.user = 'zabbix_snmp'
        self.auth_key = 'authkey123'
        self.priv_key = 'privkey123'

    def send_alert(self, message):
        try:
            errorIndication, errorStatus, errorIndex, varBinds = next(
                sendNotification(
                    SnmpEngine(),
                    UsmUserData(self.user, self.auth_key, self.priv_key,
                                authProtocol=usmHMACSHAAuthProtocol,
                                privProtocol=usmAesCfb128Protocol),
                    UdpTransportTarget((self.target_host, self.target_port)),
                    ContextData(),
                    'trap',
                    NotificationType(
                        ObjectIdentity('1.3.6.1.4.1.8072.3.2.10') # SNMP trap OID
                    ).addVarBinds(
                        ('1.3.6.1.2.1.1.1.0', OctetString(f"[{socket.gethostname()}] {message}"))
                    )
                )
            )
            if errorIndication:
                print(f"SNMP Trap Failed: {errorIndication}")
        except Exception as e:
            print(f"Failed to send SNMPv3 trap: {e}")

# Singleton instance
notifier = SNMPNotifier()

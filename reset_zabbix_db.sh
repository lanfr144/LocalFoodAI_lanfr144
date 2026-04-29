mysql -e "DROP DATABASE zabbix; CREATE DATABASE zabbix character set utf8mb4 collate utf8mb4_bin; GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'%'; FLUSH PRIVILEGES;"

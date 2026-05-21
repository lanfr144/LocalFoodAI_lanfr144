#!/bin/bash
cd /home/francois/food_project
docker-compose stop mysql
docker run -d --name mysql_temp_reset -v food_project_mysql_data:/var/lib/mysql mysql:8.0 --skip-grant-tables
sleep 7
docker exec mysql_temp_reset mysql -e "
  FLUSH PRIVILEGES;
  ALTER USER 'root'@'localhost' IDENTIFIED BY 'BTSai123';
  ALTER USER 'root'@'%' IDENTIFIED BY 'BTSai123';
  CREATE USER IF NOT EXISTS 'food_reader'@'%' IDENTIFIED BY 'BTSai123';
  ALTER USER 'food_reader'@'%' IDENTIFIED BY 'BTSai123';
  CREATE USER IF NOT EXISTS 'food_loader'@'%' IDENTIFIED BY 'BTSai123';
  ALTER USER 'food_loader'@'%' IDENTIFIED BY 'BTSai123';
  CREATE USER IF NOT EXISTS 'food_app_auth'@'%' IDENTIFIED BY 'BTSai123';
  ALTER USER 'food_app_auth'@'%' IDENTIFIED BY 'BTSai123';
  CREATE USER IF NOT EXISTS 'zabbix'@'%' IDENTIFIED BY 'BTSai123';
  ALTER USER 'zabbix'@'%' IDENTIFIED BY 'BTSai123';
  GRANT ALL PRIVILEGES ON food_db.* TO 'food_loader'@'%';
  GRANT SELECT ON food_db.* TO 'food_reader'@'%';
  GRANT SELECT, INSERT, UPDATE, DELETE ON food_db.* TO 'food_app_auth'@'%';
  GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'%';
  FLUSH PRIVILEGES;
"
docker stop mysql_temp_reset
docker rm mysql_temp_reset
docker-compose start mysql
sleep 5
docker-compose restart app ingest

#!/bin/bash
#ident "@(#)$Format:LocalFoodAI_lanfr144:reset.sh:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
cd /home/francois/food_project
docker-compose stop mysql
docker run -d --name mysql_temp_reset -v food_project_mysql_data:/var/lib/mysql mysql:8.0 --skip-grant-tables
sleep 7
docker exec mysql_temp_reset mysql -e "
  FLUSH PRIVILEGES;
  ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_db_password_here';
  ALTER USER 'root'@'%' IDENTIFIED BY 'your_db_password_here';
  CREATE USER IF NOT EXISTS 'food_reader'@'%' IDENTIFIED BY 'your_db_password_here';
  ALTER USER 'food_reader'@'%' IDENTIFIED BY 'your_db_password_here';
  CREATE USER IF NOT EXISTS 'food_loader'@'%' IDENTIFIED BY 'your_db_password_here';
  ALTER USER 'food_loader'@'%' IDENTIFIED BY 'your_db_password_here';
  CREATE USER IF NOT EXISTS 'food_app_auth'@'%' IDENTIFIED BY 'your_db_password_here';
  ALTER USER 'food_app_auth'@'%' IDENTIFIED BY 'your_db_password_here';
  CREATE USER IF NOT EXISTS 'zabbix'@'%' IDENTIFIED BY 'your_db_password_here';
  ALTER USER 'zabbix'@'%' IDENTIFIED BY 'your_db_password_here';
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
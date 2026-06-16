--ident "@(#)$Format:LocalFoodAI_lanfr144:init.sql:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
-- Create databases
CREATE DATABASE IF NOT EXISTS food_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

-- Set global flags
SET GLOBAL log_bin_trust_function_creators = 1;

-- Create/update root user for remote connections
CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY 'your_db_password_here';
ALTER USER 'root'@'%' IDENTIFIED BY 'your_db_password_here';

-- Create app users
CREATE USER IF NOT EXISTS 'food_reader'@'%' IDENTIFIED BY 'your_db_password_here';
ALTER USER 'food_reader'@'%' IDENTIFIED BY 'your_db_password_here';

CREATE USER IF NOT EXISTS 'food_loader'@'%' IDENTIFIED BY 'your_db_password_here';
ALTER USER 'food_loader'@'%' IDENTIFIED BY 'your_db_password_here';

CREATE USER IF NOT EXISTS 'food_app_auth'@'%' IDENTIFIED BY 'your_db_password_here';
ALTER USER 'food_app_auth'@'%' IDENTIFIED BY 'your_db_password_here';

CREATE USER IF NOT EXISTS 'zabbix'@'%' IDENTIFIED BY 'your_db_password_here';
ALTER USER 'zabbix'@'%' IDENTIFIED BY 'your_db_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON food_db.* TO 'food_loader'@'%';
GRANT SELECT ON food_db.* TO 'food_reader'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON food_db.* TO 'food_app_auth'@'%';
GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'%';

FLUSH PRIVILEGES;
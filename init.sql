-- Create databases
CREATE DATABASE IF NOT EXISTS food_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

-- Set global flags
SET GLOBAL log_bin_trust_function_creators = 1;

-- Create/update root user for remote connections
CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY 'BTSai123';
ALTER USER 'root'@'%' IDENTIFIED BY 'BTSai123';

-- Create app users
CREATE USER IF NOT EXISTS 'food_reader'@'%' IDENTIFIED BY 'BTSai123';
ALTER USER 'food_reader'@'%' IDENTIFIED BY 'BTSai123';

CREATE USER IF NOT EXISTS 'food_loader'@'%' IDENTIFIED BY 'BTSai123';
ALTER USER 'food_loader'@'%' IDENTIFIED BY 'BTSai123';

CREATE USER IF NOT EXISTS 'food_app_auth'@'%' IDENTIFIED BY 'BTSai123';
ALTER USER 'food_app_auth'@'%' IDENTIFIED BY 'BTSai123';

CREATE USER IF NOT EXISTS 'zabbix'@'%' IDENTIFIED BY 'BTSai123';
ALTER USER 'zabbix'@'%' IDENTIFIED BY 'BTSai123';

-- Grant privileges
GRANT ALL PRIVILEGES ON food_db.* TO 'food_loader'@'%';
GRANT SELECT ON food_db.* TO 'food_reader'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON food_db.* TO 'food_app_auth'@'%';
GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'%';

FLUSH PRIVILEGES;

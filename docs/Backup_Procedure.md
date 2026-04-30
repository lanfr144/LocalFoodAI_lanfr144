# Server Backup Procedure

This document outlines the standard operating procedure for backing up the Local Food AI application server (192.168.130.170).

## 1. MySQL Database Backup
The database contains all user accounts, parsed food profiles, and health parameters. 

**Automated Cron Backup Command:**
```bash
# Execute as the db_owner using the mysql_config_editor login path
mysqldump --login-path=app_owner --single-transaction --routines --triggers food_db > /backup/mysql/food_db_$(date +\%F).sql
```

**Zabbix Database Backup:**
```bash
mysqldump --login-path=app_owner --single-transaction --routines --triggers zabbix > /backup/mysql/zabbix_$(date +\%F).sql
```

## 2. Docker Volumes & App Data Backup
The Docker configuration, application code, and Taiga configurations must be backed up.

```bash
# Compress the entire project directory
tar -czvf /backup/app/food_project_$(date +\%F).tar.gz /home/francois/food_project/

# Backup Docker Compose configurations
tar -czvf /backup/docker/docker_configs_$(date +\%F).tar.gz /home/francois/food_project/docker/
```

## 3. Retention Policy
A standard `cron` job should be configured to run daily at `03:00 AM` local time.
To prevent disk exhaustion, backups older than 7 days should be automatically purged:
```bash
find /backup/mysql/ -type f -name "*.sql" -mtime +7 -exec rm {} \;
find /backup/app/ -type f -name "*.tar.gz" -mtime +7 -exec rm {} \;
```

## 4. Restoration Procedure
To restore the database from a backup:
```bash
mysql --login-path=app_owner food_db < /backup/mysql/food_db_2026-04-30.sql
```
To restore the application:
```bash
tar -xzvf /backup/app/food_project_2026-04-30.tar.gz -C /
cd /home/francois/food_project/docker/app
docker-compose up -d
```

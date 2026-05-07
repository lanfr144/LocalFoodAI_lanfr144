# $Id$
# Database Backup Procedure

## Automated Backups
The system utilizes a cron job pointing to `backup_db.sh`.
- The script executes `mysqldump` directly inside the MySQL container.
- Outputs are piped to `gzip` and stored in `/backups`.
- A 7-day retention policy automatically purges old backups using `find ... -mtime +7 -exec rm`.

## Manual Restore
To manually restore a backup:
`gunzip < backups/food_db_20260507_0200.sql.gz | docker exec -i food_project-mysql-1 mysql -u root -proot_pass food_db`

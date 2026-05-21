# $Id$ log fields, date format, and redesign architecture.md diagram [v1.0.2] $
# Database Backup Procedure

## Automated Backups
The system utilizes a cron job pointing to `backup_db.sh`.
- The script dynamically detects the active MySQL container name (`food-mysql-1` or `food_project-mysql-1`) for high-availability robustness.
- It executes `mysqldump` directly inside the detected MySQL container.
- Outputs are piped to `gzip` and stored in `/backups`.
- A 7-day retention policy automatically purges old backups using `find ... -mtime +7 -exec rm`.

## Manual Restore
To manually restore a backup (adjust container name to `food-mysql-1` or `food_project-mysql-1` as appropriate):
`gunzip < backups/food_db_20260507_0200.sql.gz | docker exec -i food-mysql-1 mysql -u root -proot_pass food_db`

#!/bin/bash
# backup_db.sh - Automated Disaster Recovery Backup Script

BACKUP_DIR="./backups"
DB_CONTAINER="food_project-mysql-1"
DB_NAME="food_db"
RETENTION_DAYS=7
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/food_db_$DATE.sql.gz"

echo "Starting Database Backup for $DB_NAME..."

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Execute mysqldump inside the container and pipe to gzip
sudo docker exec $DB_CONTAINER mysqldump -u root -proot_pass $DB_NAME | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup successfully saved to $BACKUP_FILE"
else
    echo "Error: Database backup failed!"
    exit 1
fi

# Apply retention policy
echo "Applying retention policy: keeping backups for $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "food_db_*.sql.gz" -type f -mtime +$RETENTION_DAYS -exec rm {} \;

echo "Backup process completed."

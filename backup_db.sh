#!/bin/bash
# $Id$
# $Author$
# $log$
#ident "@(#)LocalFoodAI:backup_db.sh:$Format:%D:%ci:%cN:%h$"
# backup_db.sh - Automated Disaster Recovery Backup Script

BACKUP_DIR="./backups"
# Detect MySQL container name dynamically (e.g. food-mysql-1 or food_project-mysql-1)
DB_CONTAINER=""
if sudo docker ps --format '{{.Names}}' | grep -q "^food-mysql-1$"; then
    DB_CONTAINER="food-mysql-1"
elif sudo docker ps --format '{{.Names}}' | grep -q "^food_project-mysql-1$"; then
    DB_CONTAINER="food_project-mysql-1"
else
    DB_CONTAINER=$(sudo docker ps --format '{{.Names}}' | grep "mysql" | head -n 1)
    if [ -z "$DB_CONTAINER" ]; then
        DB_CONTAINER="food-mysql-1"
    fi
fi
DB_NAME="food_db"
RETENTION_DAYS=7
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/food_db_$DATE.sql.gz"

echo "Starting Database Backup for $DB_NAME..."

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Load credentials from configuration file
if [ -f "./.env" ]; then
    source ./.env
fi

# Execute mysqldump inside the container securely via environment variable
sudo docker exec -e MYSQL_PWD="${MYSQL_ROOT_PASSWORD}" $DB_CONTAINER mysqldump -u root $DB_NAME | gzip > "$BACKUP_FILE"

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

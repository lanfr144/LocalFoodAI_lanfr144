#!/bin/bash
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# test_dr.sh - Automated Disaster Recovery validation script

# 1. Find the latest backup
BACKUP_DIR="./backups"
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ No backups directory found!"
    exit 1
fi

LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/food_db_*.sql.gz 2>/dev/null | head -n 1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "❌ No backup files found in $BACKUP_DIR!"
    exit 1
fi

echo "✅ Found latest backup: $LATEST_BACKUP"

# 2. Spin up a sandbox MySQL container
CONTAINER_NAME="dr_test_mysql_$(date +%s)"
echo "🚀 Spinning up sandbox MySQL container: $CONTAINER_NAME"
docker run --name "$CONTAINER_NAME" -e MYSQL_ROOT_PASSWORD=DRTestPass123! -d mysql:8.0

# 3. Wait for MySQL to be ready
echo "⏳ Waiting for MySQL to initialize..."
for i in {1..30}; do
    if docker exec "$CONTAINER_NAME" mysqladmin ping -u root -pDRTestPass123! --silent; then
        echo "✅ MySQL Sandbox is ready!"
        break
    fi
    sleep 2
    if [ "$i" -eq 30 ]; then
        echo "❌ Sandbox failed to initialize."
        docker rm -f "$CONTAINER_NAME"
        exit 1
    fi
done

# 4. Import the backup
echo "📥 Restoring backup into Sandbox..."
# Create the database first since mysqldump might not contain CREATE DATABASE if dumped without --databases
docker exec "$CONTAINER_NAME" mysql -u root -pDRTestPass123! -e "CREATE DATABASE IF NOT EXISTS food_db;"

gunzip -c "$LATEST_BACKUP" | docker exec -i "$CONTAINER_NAME" mysql -u root -pDRTestPass123! food_db

if [ $? -eq 0 ]; then
    echo "✅ Database successfully restored!"
else
    echo "❌ Failed to restore database."
    docker rm -f "$CONTAINER_NAME"
    exit 1
fi

# 5. Validation
echo "🔬 Validating data integrity..."
TABLE_COUNT=$(docker exec "$CONTAINER_NAME" mysql -u root -pDRTestPass123! -N -B -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='food_db';")
echo "📊 Found $TABLE_COUNT tables in restored database."

if [ "$TABLE_COUNT" -gt 0 ]; then
    echo "🎉 DISASTER RECOVERY TEST PASSED!"
else
    echo "❌ Validation failed: No tables found."
fi

# 6. Clean up
echo "🧹 Destroying sandbox container..."
docker rm -f "$CONTAINER_NAME" >/dev/null
echo "✅ DR Test Sequence Complete."
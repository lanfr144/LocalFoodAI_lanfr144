#!/bin/bash
# data_sync.sh - Automated Data Freshness Pipeline

LOG_DIR="./logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/data_sync.log"

# --- Auto-Detach & Sudo Auth Block ---
if [ "$1" = "--detached" ]; then
    shift # Remove --detached from arguments for normal parsing
else
    echo "Preparing to run ingestion in the background to survive SSH disconnections."
    nohup sudo "$0" --detached "$@" > "$LOG_FILE" 2>&1 < /dev/null &
    echo "Process successfully detached! You can now safely close your SSH connection."
    echo "To monitor progress at any time, type: tail -f $LOG_FILE"
    exit 0
fi
# -------------------------------------

if [ -f "./.env" ]; then
    source ./.env
fi

ONLINE_MODE=0
DATA_DIR="./data"
INGEST_FILE="en.openfoodfacts.org.products.csv"
URL="https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --online) ONLINE_MODE=1 ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

echo "Starting Data Freshness Sync at $(date)..."
mkdir -p "$DATA_DIR"

if [ "$ONLINE_MODE" -eq 1 ]; then
    echo "Online mode enabled. Checking for latest OpenFoodFacts database..."
    if ping -c 1 google.com &> /dev/null; then
        echo "Internet connection verified. Downloading latest dataset..."
        # Download strictly over HTTP to avoid certificate issues on some embedded devices
        wget -q -N -P "$DATA_DIR" "$URL"
        if [ $? -eq 0 ]; then
            echo "Download check complete."
        else
            echo "Failed to download dataset."
        fi
    else
        echo "No internet access detected. Falling back to offline mode."
    fi
else
    echo "Offline mode. Checking $DATA_DIR for manually dropped files..."
fi

# Check if file exists to trigger ingestion
if [ -f "$DATA_DIR/$INGEST_FILE" ]; then
    echo "Found dataset: $DATA_DIR/$INGEST_FILE"
    
    SHOULD_INGEST=0
    
    # 1. Checksum Validation
    NEW_CHECKSUM=$(md5sum "$DATA_DIR/$INGEST_FILE" | awk '{ print $1 }')
    OLD_CHECKSUM=""
    if [ -f "$DATA_DIR/checksum.md5" ]; then
        OLD_CHECKSUM=$(cat "$DATA_DIR/checksum.md5")
    fi
    
    if [ "$NEW_CHECKSUM" != "$OLD_CHECKSUM" ]; then
        echo "Checksum mismatch: File is new or modified. Ingestion required."
        SHOULD_INGEST=1
    else
        echo "Checksum matches previously processed file."
    fi
    
    # 2. Database Row Count Validation
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

    DB_COUNT=$(sudo docker exec -e MYSQL_PWD="${MYSQL_ROOT_PASSWORD}" "$DB_CONTAINER" mysql -u root -N -B -e "SELECT COUNT(*) FROM food_db.products_core;" 2>/dev/null)
    CSV_COUNT=$(wc -l < "$DATA_DIR/$INGEST_FILE")
    CSV_COUNT=$((CSV_COUNT - 1)) # Ignore header
    
    if [ -z "$DB_COUNT" ]; then
        DB_COUNT=0
    fi
    
    echo "Rows in DB: $DB_COUNT | Rows in CSV: $CSV_COUNT"
    if [ "$DB_COUNT" -lt "$CSV_COUNT" ]; then
        echo "Database is missing rows. Ingestion required."
        SHOULD_INGEST=1
    fi
    
    if [ "$SHOULD_INGEST" -eq 1 ]; then
        echo "Triggering ingestion pipeline via Docker Compose..."
        sudo docker-compose run --rm ingest ./ingest_csv.py "data/$INGEST_FILE"
        if [ $? -eq 0 ]; then
            echo "$NEW_CHECKSUM" > "$DATA_DIR/checksum.md5"
            echo "Ingestion complete and checksum saved."
        else
            echo "Error: Ingestion failed!"
        fi
    else
        echo "Database is fully synchronized. Skipping ingestion."
    fi
else
    echo "No dataset found in $DATA_DIR. Nothing to ingest."
fi

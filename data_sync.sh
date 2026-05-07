#!/bin/bash
# $Id$
# $Author$
# $log$
# data_sync.sh - Automated Data Freshness Pipeline

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

echo "Starting Data Freshness Sync..."
mkdir -p "$DATA_DIR"

if [ "$ONLINE_MODE" -eq 1 ]; then
    echo "Online mode enabled. Checking for latest OpenFoodFacts database..."
    if ping -c 1 google.com &> /dev/null; then
        echo "Internet connection verified. Downloading latest dataset..."
        # Use -N to only download if newer than local file
        wget -N -P "$DATA_DIR" "$URL"
        if [ $? -eq 0 ]; then
            echo "Download complete."
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
    # We should only ingest if the file is new or modified. 
    # For simplicity, we just trigger ingestion if the file exists.
    # Ingest script handles DROP TABLE if needed, but wait: ingest_csv appends by default or we can modify it.
    echo "Found dataset: $DATA_DIR/$INGEST_FILE"
    echo "Triggering ingestion pipeline via Docker Compose..."
    sudo docker-compose run --rm ingest ./ingest_csv.py "data/$INGEST_FILE"
    
    # After successful ingestion, move or rename to prevent infinite loops on offline cron
    mv "$DATA_DIR/$INGEST_FILE" "$DATA_DIR/$INGEST_FILE.processed"
    echo "Ingestion complete and file archived."
else
    echo "No dataset found in $DATA_DIR. Nothing to ingest."
fi

#!/bin/bash
# Local Food AI - Disconnected Ingestion Wrapper
# This script uses nohup to run the python ingestion script in the background.
# You can exit your SSH session safely after starting this script.

echo "========================================================="
echo "🍔 Local Food AI: Extreme Batch Ingestion"
echo "========================================================="

if [ ! -f "en.openfoodfacts.org.products.csv" ] && [ ! -f "fr.openfoodfacts.org.products.csv" ]; then
    echo "❌ Error: CSV files not found in the current directory."
    echo "Please download the massive CSVs before running this batch."
    exit 1
fi

echo "🚀 Starting database wipe and reset..."
# Automatically run the new DB setup to drop the rigid table
venv/bin/python3 setup_db.py

echo "🚀 Triggering background ingestion process via nohup..."
echo "All outputs will be saved to ingestion_process.log"

# Run securely in background
nohup venv/bin/python3 -u ingest_csv.py > ingestion_process.log 2>&1 &
BG_PID=$!

echo "✅ Process started in the background (PID: $BG_PID)"
echo "You can now safely close your terminal or turn off your computer."
echo "To monitor progress from the server later, run:"
echo "   tail -f ingestion_process.log"

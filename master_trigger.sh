#!/bin/bash
# Natively reload all database logic without interactive blocks
echo "Executing autonomous WSL reload..."
pip3 install --break-system-packages pymysql pandas sqlalchemy sqlalchemy-utils cryptography openpyxl
python3 setup_db.py
echo "Spawning Batch Ingestion into background..."
nohup bash start_batch_ingest.sh > ingest_log.txt 2>&1 &
echo "Master pipeline triggered successfully."

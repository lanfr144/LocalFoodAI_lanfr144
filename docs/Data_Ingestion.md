# Data Ingestion Guide

The Local Food AI relies on the OpenFoodFacts dataset. Because this dataset is massive (~24GB), a specialized ingestion pipeline was built to bypass MySQL InnoDB row limits.

## The Architecture
The database is structured using **Grouped Vertical Partitioning**. Instead of a single monolithic table with 200+ columns, data is sliced into 5 distinct tables:
1. `products_core` (Names, text, ingredients)
2. `products_allergens` (Allergy data)
3. `products_macros` (Fats, proteins, carbs, etc. as `DOUBLE`)
4. `products_vitamins` (Vitamin traces)
5. `products_minerals` (Mineral traces)

A MySQL `VIEW` named `products` elegantly joins these together so the frontend can query them seamlessly.

## How to Ingest
1. Download the CSV using `download_csv.sh`. It will fetch `en.openfoodfacts.org.products.csv`.
2. Do **not** run the ingestion script directly in the terminal, as SSH disconnects will kill the process.
3. Use the `nohup` wrapper:
   ```bash
   nohup bash ./start_batch_ingest.sh > remote_ingest.log 2>&1 &
   ```
4. You can monitor the ingestion progress by tailing the logs:
   ```bash
   tail -f ingestion_process.log
   ```

## Script Internals
The `ingest_csv.py` uses `pandas` chunking (`chunksize=10000`). For every chunk, it slices the DataFrame into the 5 partitions and executes an `INSERT IGNORE` into the MySQL database. This ensures robustness and allows the script to be safely interrupted and restarted.

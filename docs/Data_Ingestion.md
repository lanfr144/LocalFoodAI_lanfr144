# $Id: 1701828b122e0c319e59134ca6511a42ecad9297 Lange François lanfr144@school.lu 2026/06/11 08:26:59 Lange François lanfr144@school.lu 2026/06/11 08:26:59   [TG-131] Purge database passwords from tracked files and format application versioning [PreRelease-1.0-26-g1701828] $
# Data Ingestion Pipeline

## Overview
The application utilizes `data_sync.sh` to update the OpenFoodFacts dataset.

## Online Mode
Run `bash data_sync.sh --online`. The script will download the latest CSV directly from the official servers and trigger the ingestion pipeline.

## Offline Mode
Drop a `en.openfoodfacts.org.products.csv` file into the `/data` folder and run `bash data_sync.sh`. The script detects the file and triggers the Docker ingestion container.

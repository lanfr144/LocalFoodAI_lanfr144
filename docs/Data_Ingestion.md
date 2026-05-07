# $Id$
# Data Ingestion Pipeline

## Overview
The application utilizes `data_sync.sh` to update the OpenFoodFacts dataset.

## Online Mode
Run `bash data_sync.sh --online`. The script will download the latest CSV directly from the official servers and trigger the ingestion pipeline.

## Offline Mode
Drop a `en.openfoodfacts.org.products.csv` file into the `/data` folder and run `bash data_sync.sh`. The script detects the file and triggers the Docker ingestion container.

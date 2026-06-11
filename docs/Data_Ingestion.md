# $Id: 03cbc893f143c3ae43fc35e97913bedb89b41e23 Lange François lanfr144@school.lu 2026/06/11 10:38:26 Lange François lanfr144@school.lu 2026/06/11 10:38:26   [#1] chore: fix git-ident-filter self-modification regex bug by concatenating search strings [PreRelease-1.0-28-g03cbc89] $
# Data Ingestion Pipeline

## Overview
The application utilizes `data_sync.sh` to update the OpenFoodFacts dataset.

## Online Mode
Run `bash data_sync.sh --online`. The script will download the latest CSV directly from the official servers and trigger the ingestion pipeline.

## Offline Mode
Drop a `en.openfoodfacts.org.products.csv` file into the `/data` folder and run `bash data_sync.sh`. The script detects the file and triggers the Docker ingestion container.

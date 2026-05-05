#!/bin/bash
# download latest OpenFoodFacts CSVs if not present or if newer version exists
DATA_DIR="$(dirname "$0")/data"
mkdir -p "$DATA_DIR"

EN_URL="https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv"
FR_URL="https://static.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv"

EN_FILE="$DATA_DIR/en.openfoodfacts.org.products.csv"
FR_FILE="$DATA_DIR/fr.openfoodfacts.org.products.csv"

download() {
  local url=$1
  local file=$2
  if [ -f "$file" ]; then
    echo "File $file already exists, checking for updates..."
    curl -z "$file" -L -o "$file" "$url"
  else
    echo "Downloading $url..."
    curl -L -o "$file" "$url"
  fi
}

download "$EN_URL" "$EN_FILE"

download "$FR_URL" "$FR_FILE"

echo "CSV download completed."

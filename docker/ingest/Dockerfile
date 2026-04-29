# Dockerfile for ingestion service
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements (if any) – using existing requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy ingestion script and any helpers
COPY ingest_csv.py ./
COPY myloginpath.py ./

# Entry point (will be overridden by K8s job)
CMD ["python", "ingest_csv.py"]

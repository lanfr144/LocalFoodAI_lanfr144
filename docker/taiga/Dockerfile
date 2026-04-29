# Dockerfile for Taiga sync service
FROM python:3.11-slim

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Taiga sync scripts (assumed to be in project root)
COPY taiga_feed.py ./
COPY generate_taiga_wiki.py ./
COPY taiga_checker.py ./

# Wrapper script to gracefully skip when no Taiga URL/token
COPY run_sync.sh /app/run_sync.sh
RUN chmod +x /app/run_sync.sh

CMD ["/app/run_sync.sh"]

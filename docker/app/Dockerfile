# Dockerfile for Streamlit UI
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py ./
COPY myloginpath.py ./


EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true"]

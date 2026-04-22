#!/bin/bash
# Local Food AI - SearXNG Setup (Docker)

echo "========================================================="
echo "🔍 Installing Docker & SearXNG Locally"
echo "========================================================="

echo "[1/4] Installing Docker..."
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker

echo "[2/4] Setting up SearXNG environment structure..."
sudo mkdir -p /etc/searxng

echo "[3/4] Generating strict local AI settings.yml..."
# We explicitly enable JSON formats so the python app can scrape the API invisibly
sudo cat << 'EOF' > /etc/searxng/settings.yml
use_default_settings: true
general:
  debug: false
  instance_name: "Local Food AI Search"
search:
  safe_search: 0
  autocomplete: ""
  default_lang: "en"
  formats:
    - html
    - json
server:
  port: 8080
  bind_address: "0.0.0.0"
  secret_key: "ai_food_search_secret_key"
  limiter: false
  image_proxy: true
EOF

echo "[4/4] Launching official SearXNG Container..."
# Bind strictly to localhost (127.0.0.1) so no one outside the VM can hit the search engine
sudo docker stop searxng 2>/dev/null || true
sudo docker rm searxng 2>/dev/null || true

sudo docker run -d \
  -p 127.0.0.1:8080:8080 \
  -v /etc/searxng:/etc/searxng \
  --name searxng \
  --restart always \
  searxng/searxng

echo "✅ SearXNG is now running firmly isolated on http://127.0.0.1:8080!"

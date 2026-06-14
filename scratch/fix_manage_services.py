import re
import os

file_path = "manage_services.sh"
with open(file_path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# Replace encoding issues in header
content = content.replace("Lange Franois", "Francois Lange")
content = content.replace("Lange FranA ois", "Francois Lange")

# 1. Update COMPOSE_FILE logic
old_compose = 'COMPOSE_FILE="docker-compose.yml"'
new_compose = """COMPOSE_FILE="docker-compose.yml"
# Auto-detect WSL context and use port-shifted docker-compose-wsl.yml
if [ -f "docker-compose-wsl.yml" ] && (grep -qi "microsoft" /proc/sys/kernel/osrelease 2>/dev/null || grep -qi "wsl" /proc/sys/kernel/osrelease 2>/dev/null); then
    COMPOSE_FILE="docker-compose-wsl.yml"
fi"""

content = content.replace(old_compose, new_compose)

# 2. Update mysqladmin ping readiness check
old_ping = """    # Wait for MySQL to become fully ready and accept connections
    log_info "Waiting for MySQL database socket to be available..."
    until docker compose -f "$COMPOSE_FILE" exec mysql mysqladmin ping -h"localhost" -u"root" -p"your_db_password_here" --silent; do
        sleep 2
        echo -n "."
    done"""

new_ping = """    # Wait for MySQL to become fully ready and accept connections
    log_info "Waiting for MySQL database socket to be available..."
    DB_ROOT_PASS="your_db_password_here"
    if [ -f "./.env" ]; then
        ENV_PASS=$(grep '^[ \\t]*MYSQL_ROOT_PASSWORD[ \\t]*=' .env | sed 's/^.*=//' | tr -d '\\r\\n ')
        if [ ! -z "$ENV_PASS" ]; then
            DB_ROOT_PASS="$ENV_PASS"
        fi
    fi
    until docker compose -f "$COMPOSE_FILE" exec mysql mysqladmin ping -h"localhost" -u"root" -p"$DB_ROOT_PASS" --silent; do
        sleep 2
        echo -n "."
    done"""

content = content.replace(old_ping, new_ping)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("manage_services.sh successfully updated and encoding sanitized.")

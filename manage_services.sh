#!/bin/bash
#ident "@(#)$Format:LocalFoodAI_lanfr144:manage_services.sh:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# ==============================================================================
# File: manage_services.sh
# Purpose: Comprehensive Service Manager for Local Food AI development.
#          Allows operators and developers to cleanly start, stop, restart,
#          and inspect all project elements in sequential order of dependencies
#          without triggering online data ingestion pipelines.
# ==============================================================================

# Exit immediately if a command exits with a non-zero status (except when checked)
set -e

# Sequence priority rules:
# STARTUP:  1. MySQL -> 2. Ollama & SearXNG -> 3. Streamlit App & Nginx Proxy -> 4. Zabbix & Airflow
# SHUTDOWN: 1. Zabbix & Airflow -> 2. Nginx & App -> 3. SearXNG & Ollama -> 4. MySQL

COMPOSE_FILE="docker-compose.yml"
# Auto-detect WSL context and use port-shifted docker-compose-wsl.yml
if [ -f "docker-compose-wsl.yml" ] && (grep -qi "microsoft" /proc/sys/kernel/osrelease 2>/dev/null || grep -qi "wsl" /proc/sys/kernel/osrelease 2>/dev/null); then
    COMPOSE_FILE="docker-compose-wsl.yml"
fi

# Colors for output logging
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $1${NC}"
}

log_success() {
    echo -e "${GREEN}[SUCCESS] $(date '+%Y-%m-%d %H:%M:%S') - $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}[WARNING] $(date '+%Y-%m-%d %H:%M:%S') - $1${NC}"
}

log_error() {
    echo -e "${RED}[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $1${NC}"
}

# Verify Docker Compose file exists
if [ ! -f "$COMPOSE_FILE" ]; then
    log_error "Docker Compose file ($COMPOSE_FILE) not found in the current directory."
    exit 1
fi

start_services() {
    log_info "Initiating sequential startup sequence for development..."

    # Step 1: Start MySQL Database
    log_info "Step 1/4: Starting MySQL Database Container..."
    docker compose -f "$COMPOSE_FILE" up -d mysql
    
    # Wait for MySQL to become fully ready and accept connections
    log_info "Waiting for MySQL database socket to be available..."
    DB_ROOT_PASS="your_db_password_here"
    if [ -f "./.env" ]; then
        ENV_PASS=$(grep '^[ \t]*MYSQL_ROOT_PASSWORD[ \t]*=' .env | sed 's/^.*=//' | tr -d '\r\n ')
        if [ ! -z "$ENV_PASS" ]; then
            DB_ROOT_PASS="$ENV_PASS"
        fi
    fi
    until docker compose -f "$COMPOSE_FILE" exec mysql mysqladmin ping -h"localhost" -u"root" -p"$DB_ROOT_PASS" --silent; do
        sleep 2
        echo -n "."
    done
    echo ""
    log_success "MySQL is online and healthy."

    # Step 2: Start local AI Engine (Ollama) and Anonymous Search (SearXNG)
    log_info "Step 2/4: Starting Ollama and SearXNG microservices..."
    docker compose -f "$COMPOSE_FILE" up -d ollama searxng
    
    # Wait briefly for Ollama daemon bind
    sleep 3
    log_success "AI and Search infrastructure successfully online."

    # Step 3: Start Core Streamlit Application UI and Nginx Gateway Proxy
    log_info "Step 3/4: Starting Streamlit UI and Nginx Proxy Gateway..."
    docker compose -f "$COMPOSE_FILE" up -d app nginx
    log_success "Frontend and Proxy elements online."

    # Step 4: Start DevOps Orchestrator Stack (Zabbix Monitoring, Zabbix Agent, Airflow)
    log_info "Step 4/4: Deploying Zabbix Monitoring suite and Airflow Supervisors..."
    # Note: Airflow scheduler/webserver are started for pipeline supervision
    docker compose -f "$COMPOSE_FILE" up -d zabbix-server zabbix-web zabbix-agent
    
    # Check if Airflow service elements exist in compose file before starting
    if grep -q "airflow-webserver" "$COMPOSE_FILE"; then
        docker compose -f "$COMPOSE_FILE" up -d airflow-webserver airflow-scheduler || log_warn "Airflow containers not defined or failed to start."
    fi

    log_success "All Local Food AI development services started successfully!"
}

stop_services() {
    log_info "Initiating sequential graceful shutdown sequence..."

    # Step 1: Stop Monitoring and Supervisor Stack
    log_info "Step 1/4: Stopping Zabbix suite and Airflow Supervisors..."
    docker compose -f "$COMPOSE_FILE" stop zabbix-agent zabbix-web zabbix-server
    if grep -q "airflow-webserver" "$COMPOSE_FILE"; then
        docker compose -f "$COMPOSE_FILE" stop airflow-scheduler airflow-webserver || true
    fi
    log_success "DevOps monitoring stack shut down."

    # Step 2: Stop Streamlit Application and Secure Proxy Gateway
    log_info "Step 2/4: Shutting down Nginx and App frontend..."
    docker compose -f "$COMPOSE_FILE" stop nginx app
    log_success "Application frontend shut down."

    # Step 3: Stop AI Ollama Inference Engine and SearXNG Search Gateway
    log_info "Step 3/4: Stopping SearXNG and Ollama AI Engine..."
    docker compose -f "$COMPOSE_FILE" stop searxng ollama
    log_success "AI services shut down."

    # Step 4: Stop Core MySQL Database Container gracefully (prevent table corruption)
    log_info "Step 4/4: Stopping MySQL database..."
    docker compose -f "$COMPOSE_FILE" stop mysql
    log_success "Database node cleanly shut down."

    log_success "All Local Food AI services stopped gracefully!"
}

check_status() {
    log_info "Inspecting status of stack containers..."
    docker compose -f "$COMPOSE_FILE" ps
    
    log_info "Active network sockets check:"
    echo "---------------------------------------------------------"
    echo "Port  | Target Service               | Status"
    echo "---------------------------------------------------------"
    
    # Check MySQL on 3307
    if nc -z localhost 3307 2>/dev/null; then
        echo -e "3307  | MySQL Database Node          | ${GREEN}ONLINE${NC}"
    else
        echo -e "3307  | MySQL Database Node          | ${RED}OFFLINE${NC}"
    fi

    # Check Ollama on 11434
    if nc -z localhost 11434 2>/dev/null; then
        echo -e "11434 | Ollama AI Engine             | ${GREEN}ONLINE${NC}"
    else
        echo -e "11434 | Ollama AI Engine             | ${RED}OFFLINE${NC}"
    fi

    # Check Nginx Gateway on 80
    if nc -z localhost 80 2>/dev/null; then
        echo -e "80    | Nginx Gateway (HTTP Proxy)   | ${GREEN}ONLINE${NC}"
    else
        echo -e "80    | Nginx Gateway (HTTP Proxy)   | ${RED}OFFLINE${NC}"
    fi

    # Check Zabbix Web UI on 8081
    if nc -z localhost 8081 2>/dev/null; then
        echo -e "8081  | Zabbix Dashboard             | ${GREEN}ONLINE${NC}"
    else
        echo -e "8081  | Zabbix Dashboard             | ${RED}OFFLINE${NC}"
    fi
    echo "---------------------------------------------------------"
}

show_help() {
    echo "Usage: $0 {start|stop|restart|status}"
    echo "  start   - Deploy and wake up all services sequentially according to priorities."
    echo "  stop    - Gracefully turn off containers in reverse dependency order."
    echo "  restart - Perform sequential shutdown followed by sequential boot."
    echo "  status  - Print container status and inspect physical TCP port sockets."
    exit 1
}

case "$1" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        stop_services
        start_services
        ;;
    status)
        check_status
        ;;
    *)
        show_help
        ;;
esac
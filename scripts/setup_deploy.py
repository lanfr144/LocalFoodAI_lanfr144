import os
import sys
import getpass

import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

print("="*60)
print(" Local Food AI - Distributed Deployment Configuration Tool")
print("="*60)

# Check Docker availability
try:
    subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("[+] Docker is correctly configured and accessible.")
except (subprocess.CalledProcessError, FileNotFoundError):
    print("[-] Warning: Docker is not running or not accessible. Please ensure Docker Desktop or Docker Engine is installed and running before deploying.")

print("\nSelect the role for this specific node in the network:")
print("1. All-in-One (Runs everything, default)")
print("2. Application Frontend (Runs Streamlit, Nginx, AI Services)")
print("3. Database Node (Runs MySQL & Ingestion)")
print("4. Monitoring Node (Runs Zabbix Server & UI)")

choice = input("\nEnter choice (1-4) [1]: ").strip() or "1"

# Environment Variables
env_vars = {}

if choice != "1":
    print("\n--- Network Configuration ---")
    if choice != "3":
        env_vars['DB_HOST'] = input("Enter the IP address of the Database Node: ").strip()
    else:
        env_vars['DB_HOST'] = "mysql"
        
    if choice != "4":
        env_vars['ZBX_SERVER_HOST'] = input("Enter the IP address of the Monitoring Node: ").strip()
    else:
        env_vars['ZBX_SERVER_HOST'] = "zabbix-server"
else:
    env_vars['DB_HOST'] = "mysql"
    env_vars['ZBX_SERVER_HOST'] = "zabbix-server"

print("\n--- Security Configuration ---")
env_vars['MYSQL_ROOT_PASSWORD'] = getpass.getpass("Enter MySQL Root Password (will not echo): ")
env_vars['DB_READER_PASS'] = getpass.getpass("Enter DB Reader Password: ")
env_vars['DB_LOADER_PASS'] = getpass.getpass("Enter DB Loader Password: ")
env_vars['DB_APP_AUTH_PASS'] = getpass.getpass("Enter App Auth Password: ")
env_vars['MYSQL_ZABBIX_PASSWORD'] = getpass.getpass("Enter Zabbix DB Password: ")

# Generate .env
print("\n[+] Generating .env file...")
with open(".env", "w") as f:
    for k, v in env_vars.items():
        f.write(f"{k}={v}\n")

# Base compose dictionaries
compose_services = {}

mysql_service = """
  mysql:
    build:
      context: ./docker/mysql
    ports:
      - "3307:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./my.cnf:/etc/mysql/conf.d/custom_ai_app.cnf
      - ./init.sql:/docker-entrypoint-initdb.d/1-init.sql
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 20
    restart: always
"""

ingest_service = """
  ingest:
    build:
      context: .
      dockerfile: docker/ingest/Dockerfile
    environment:
      - DB_HOST=${DB_HOST}
      - DB_USER=food_loader
      - DB_PASS=${DB_LOADER_PASS}
    volumes:
      - ./:/app
    profiles:
      - manual
"""

ai_services = """
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    restart: always

  searxng:
    image: searxng/searxng:latest
    ports:
      - "8080:8080"
    volumes:
      - ./searxng:/etc/searxng
    environment:
      - SEARXNG_BASE_URL=http://localhost:8080/
    restart: always
"""

app_service = """
  app:
    build:
      context: .
      dockerfile: docker/app/Dockerfile
    ports:
      - "8502:8501"
    environment:
      - DB_HOST=${DB_HOST}
      - DB_USER=food_reader
      - DB_PASS=${DB_READER_PASS}
      - APP_AUTH_USER=food_app_auth
      - APP_AUTH_PASS=${DB_APP_AUTH_PASS}
      - OLLAMA_HOST=http://ollama:11434
      - SEARXNG_HOST=http://searxng:8080
    restart: always

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    restart: always
"""

monitoring_services = """
  zabbix-server:
    image: zabbix/zabbix-server-mysql:ubuntu-7.0-latest
    environment:
      - DB_SERVER_HOST=${DB_HOST}
      - MYSQL_USER=zabbix
      - MYSQL_PASSWORD=${MYSQL_ZABBIX_PASSWORD}
      - ZBX_SNMPTRAPPER=1
    restart: always
    ports:
      - "10051:10051"

  zabbix-web:
    image: zabbix/zabbix-web-nginx-mysql:ubuntu-7.0-latest
    ports:
      - "8081:8080"
      - "8444:8443"
    environment:
      - DB_SERVER_HOST=${DB_HOST}
      - MYSQL_USER=zabbix
      - MYSQL_PASSWORD=${MYSQL_ZABBIX_PASSWORD}
      - ZBX_SERVER_HOST=zabbix-server
      - PHP_TZ=Europe/Paris
    restart: always

  zabbix-agent:
    image: zabbix/zabbix-agent:ubuntu-7.0-latest
    environment:
      - ZBX_HOSTNAME=DistributedNode
      - ZBX_SERVER_HOST=${ZBX_SERVER_HOST}
    privileged: true
    pid: "host"
    volumes:
      - /var/run:/var/run
    restart: always
"""

header = "services:\n"
footer = """
volumes:
  mysql_data:
  ollama_data:
"""

compose_content = header

if choice == "1":
    compose_content += mysql_service + ingest_service + ai_services + app_service + monitoring_services
elif choice == "2":
    compose_content += ai_services + app_service
    footer = "volumes:\n  ollama_data:\n"
elif choice == "3":
    compose_content += mysql_service + ingest_service
    footer = "volumes:\n  mysql_data:\n"
elif choice == "4":
    compose_content += monitoring_services
    footer = ""

print("\n[+] Generating docker-compose.yml for selected role...")
with open("docker-compose.yml", "w") as f:
    f.write(compose_content + footer)

print("\n" + "="*60)
print("⚠️ IMPORTANT HYPERVISOR NETWORKING REMINDER:")
print("If this node is running inside VirtualBox or Hyper-V, you MUST configure the VM network adapter to use a 'Bridged Adapter' or 'External Virtual Switch' so it shares the host's subnet. Otherwise, cross-node communication will fail.")
print("="*60)

print("\nDone! You can now run `docker compose up -d`.")

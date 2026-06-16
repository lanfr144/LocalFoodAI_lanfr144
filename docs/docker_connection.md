# Docker Connection & Health Check Guide
The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:docker_connection.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

This document explains how to interact with the various Docker containers that power the Local Food AI system.

## Starting the Stack
To start the application and all its microservices:
```bash
# Standard environment
docker-compose up -d

# Windows / WSL environment (if applicable)
docker-compose -f docker-compose-wsl.yml up -d
```

## Connecting to Specific Containers

### 1. MySQL Database
To access the MySQL shell directly:
```bash
docker exec -it food-mysql-1 mysql -u root -p
```
*Note: The password is defined in your `.env` file (`MYSQL_ROOT_PASSWORD`).*

### 2. Ollama (AI Engine)
To manage LLM models or test the AI engine:
```bash
docker exec -it food-ollama-1 bash
# Inside the container, you can run:
# ollama list
# ollama run qwen2.5:1.5b
```

### 3. SearXNG (Web Search)
To view the SearXNG logs if the web search context is failing:
```bash
docker logs -f food-searxng-1
```

### 4. Zabbix (Telemetry)
If you need to access the Zabbix server or agent:
```bash
docker exec -it food-zabbix-server-1 bash
```

## Health Checks
You can verify that all application components are working using:
```bash
docker ps
```
Look for `Up (healthy)` in the STATUS column for the `mysql` service, and ensure `food-app-1` (Streamlit) is running without restarting.
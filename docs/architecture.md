# Local Food AI: Architecture Map

## 1. Core Stack
- **Database**: MySQL 8.0 (Partitioned for 3GB+ OpenFoodFacts dataset).
- **Backend & Frontend**: Python 3.11 with Streamlit.
- **AI Engine**: Ollama running locally with `llama3.2:1b` (quantized for 30GB RAM limits).
- **Web Search**: SearXNG Private Engine (used dynamically when the local DB lacks specific food heuristics).
- **Monitoring**: Zabbix Telemetry Server (connected via native Python SNMP traps and container-level SNMP daemons).

## 2. Security Infrastructure
- **Zero Cloud Policy**: 100% of the AI processing, Database searching, and Telemetry happens locally on the Ubuntu VM. No user dietary queries leave the machine.
- **Principle of Least Privilege (PoLP)**:
  - `db_app_auth`: Only has access to the authentication tables.
  - `db_reader`: Only has `SELECT` privileges on the food partitions.
  - `db_loader`: Only has `INSERT` privileges for the background CSV script.
- **Encryption**: User passwords are mathematically salted and hashed using `bcrypt` (Blowfish cipher).

## 3. Distributed Microservice Networking
This stack is designed to be highly decoupled. While typically run via a unified `docker-compose.yml`, the application supports distributed routing across:
1. WSL2 Nodes (Frontend App)
2. Hyper-V Instances (MySQL Partition Clusters)
3. VirtualBox Hosts (Ollama GPU/CPU compute nodes)
*(Refer to `distributed_deployment.md` for specific Bridged Adapter setups).*

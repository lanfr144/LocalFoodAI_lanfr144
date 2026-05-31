# 🚀 WSL2 Port-Shifted Installation Guide (Local Food AI)

This guide provides step-by-step instructions to install and run the **Local Food AI** system on Windows Subsystem for Linux (WSL2).

To prevent port conflicts with standard local services (such as existing MySQL databases, custom Nginx web ports, Zabbix suites, or Airflow installations), all public host ports in this deployment have been increased by **+20** from their original defaults.

---

## 📊 Port Mapping Reference

| Service Container | Original Port | Shifted Port (+20) | Type / Purpose |
| :--- | :---: | :---: | :--- |
| **Nginx Proxy** | `80` | **`100`** *(or `8020`)* | Main Web Gateway (Reverse Proxy) |
| **Streamlit Application** | `8502` | **`8522`** | Direct Streamlit web port |
| **MySQL Database** | `3306` | **`3326`** | Database external connection listener |
| **SearXNG Search** | `8085` | **`8105`** | Anonymous meta-search gateway |
| **Zabbix Web UI** | `8081` / `8444` | **`8101`** / **`8464`** | Monitoring dashboard (HTTP / HTTPS) |
| **Zabbix Server Daemon** | `10051` | **`10071`** | Active telemetry monitoring trap listener |
| **Airflow Webserver** | `8082` | **`8102`** | Airflow data workflow manager |

---

## 🛠️ Step-by-Step Installation Runbook

### Step 1: Open Your WSL2 Ubuntu Terminal
Ensure you have WSL2 enabled and are using an Ubuntu 24.04 shell instance.

### Step 2: Clone the Git Repository
Run the following commands inside your WSL Ubuntu home directory to clone the project:
```bash
git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git
cd LocalFoodAI_lanfr144
```

### Step 3: Setup Local Environment Variables
Create the required `.env` file at the root of the repository to feed standard local credentials to the containers:
```bash
cat <<EOF > .env
MYSQL_ROOT_PASSWORD=BTSai123
DB_READER_PASS=BTSai123
DB_LOADER_PASS=BTSai123
DB_APP_AUTH_PASS=BTSai123
MYSQL_ZABBIX_PASSWORD=BTSai123
EOF
```

### Step 4: Launch the Docker Container Stack
Deploy the entire 10-container system in the background using the custom port-shifted WSL configuration file:
```bash
docker compose -f docker-compose-wsl.yml up -d
```

### Step 5: Pull the Quantized Reasoning LLM Model
Download the high-capacity, reasoning-optimized local model **`qwen2.5:7b`** directly inside the running Ollama container instance:
```bash
docker exec -it $(docker ps -q -f name=ollama) ollama pull qwen2.5:7b
```

### Step 6: Ingest the OpenFoodFacts Database Records
Initialize the database tables and trigger the ingestion pipeline to parse local dataset records:
```bash
docker compose -f docker-compose-wsl.yml run --rm ingest python ingest_csv.py
```

---

## 🌐 Verifying and Accessing the Services

Once the stack is fully running, you can connect to all system components in your web browser:

*   **🍏 Streamlit Application UI**: Open `http://localhost:100` *(uses Nginx reverse proxy on Port 100)* or bypass the proxy directly at `http://localhost:8522`.
*   **📊 Zabbix Monitoring Suite**: Open `http://localhost:8101` *(Default Credentials: Username `Admin` / Password `zabbix`)*.
*   **🌀 Airflow Dag Orchestrator**: Open `http://localhost:8102` *(Default Credentials: Username `admin` / Password `admin`)*.
*   **🔍 Database Server**: Connect using your preferred SQL client (DBeaver, MySQL Workbench) via Host `localhost` and Port `3326`.

---

*Prepared by Francois Lange for the Local Food AI Delivery.*

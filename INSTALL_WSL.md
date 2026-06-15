The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:INSTALL_WSL.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

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

**Primary Repository (Internal Network)**:
```bash
git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git
cd LocalFoodAI_lanfr144
```

**Alternative Repository (Worldwide Access - Clone of the Primary)**:
```bash
git clone https://github.com/lanfr144/LocalFoodAI_lanfr144.git
cd LocalFoodAI_lanfr144
```

### Step 3: Setup Local Environment Variables
Create the required `.env` file at the root of the repository to feed standard local credentials to the containers:
Configure your database credentials, active network mode, and the target model name in a `.env` file at the root of the repository. A generic template is provided below:

```ini
# NETWORK_MODE: local (offline) or server (online)
NETWORK_MODE=local
LLM_MODEL=llama3.2:3b

# DATABASE CREDENTIALS (MySQL)
MYSQL_ROOT_PASSWORD=your_secure_root_password
DB_READER_PASS=your_secure_reader_password
DB_LOADER_PASS=your_secure_loader_password
DB_APP_AUTH_PASS=your_secure_auth_password
MYSQL_ZABBIX_PASSWORD=your_secure_zabbix_password

# ZABBIX & SNMP CREDENTIALS
ZABBIX_USER=Admin
ZABBIX_PASS=zabbix
ZABBIX_SNMP_USER=zabbix_snmp
ZABBIX_SNMP_AUTHKEY=authkey123
ZABBIX_SNMP_PRIVKEY=privkey123
DISCORD_WEBHOOK=https://discord.com/api/webhooks/your_webhook_id

# EMAIL ALERTS CONFIGURATION
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_app_password

# TAIGA CREDENTIALS
TAIGA_URL=https://192.168.130.161/taiga
TAIGA_USER=your_taiga_user
TAIGA_PASS=your_taiga_password
```

### Step 4: Launch the Docker Container Stack
Deploy the entire 10-container system in the background using the custom port-shifted WSL configuration file:
```bash
docker compose -f docker-compose-wsl.yml up -d
```

### Step 5: Pull the Quantized Reasoning LLM Model
Download the high-capacity, reasoning-optimized local model directly inside the running Ollama container instance:
```bash
docker exec -it $(docker ps -q -f name=ollama) ollama pull $( grep '^[ \t]*LLM_MODEL[ 	]*=' .env | sed 's/^.*=//' )
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

## ⚡ Developer Productivity & Troubleshooting

### 1. Dynamic LLM Pulls (Non-Interactive)
To pull updates to your reasoning models in a single line without entering an interactive shell, use:
```bash
docker exec -it $(docker ps -q -f name=ollama) ollama pull $(grep '^[ \t]*LLM_MODEL[ \t]*=' .env | cut -d'=' -f2)
```

### 2. Path Resolutions inside WSL
If you need to configure container volumes or load local files (like the datasets or PDF fonts), remember that the host's `C:` drive is mounted under `/mnt/c/` in WSL:
* **Windows Path:** `C:/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/docs/fonts/`
* **WSL Path:** `/mnt/c/Users/lanfr144/Documents/DOPRO1/Antigravity/Food/docs/fonts/`
* *Tip:* Always use forward slashes `/` in path configurations, as they are natively supported by both PowerShell on the Windows host and Bash inside WSL.

### 3. Git Attributes Clean/Smudge Loops
If running a clean checkout (e.g. `git checkout -f`) triggers an error about a missing `git-ident-filter.py` script, restore the filter script first before executing the checkout:
```bash
git checkout HEAD -- local_tools/git-ident-filter.py
git checkout -f
```

---

*Prepared by Francois Lange for the Local Food AI Delivery.*
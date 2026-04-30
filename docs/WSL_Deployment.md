# WSL Deployment Playbook

This document describes how to deploy the entire Local Food AI stack (including the database, Streamlit app, and Zabbix monitoring) into a fresh Windows Subsystem for Linux (WSL) environment.

## 1. Prerequisites
Open PowerShell as Administrator and install WSL (Ubuntu):
```powershell
wsl --install -d Ubuntu
```

Once inside the WSL Ubuntu terminal, update the package manager:
```bash
sudo apt update && sudo apt upgrade -y
```

## 2. Install Dependencies
Install MySQL Server, Docker, and Python:
```bash
# Install MySQL
sudo apt install mysql-server -y
sudo systemctl start mysql

# Install Docker
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER

# Install Python and SNMP utilities
sudo apt install python3-pip python3-venv snmp snmpd snmptrapd -y
```

## 3. Clone Repository
Clone the project repository from the Taiga/Git hub:
```bash
git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git food_project
cd food_project
```

## 4. Initialize Database
Run the setup script to provision the MySQL database and securely create the PoLP users.
```bash
sudo python3 setup_db.py
```
*(You will be prompted for the MySQL root password, which is blank by default on fresh WSL installs. Press Enter).*

## 5. Configure Secure Credentials
Establish the `mysql_config_editor` login paths so the application can connect to the database without exposing raw passwords.
```bash
mysql_config_editor set --login-path=app_auth --host=127.0.0.1 --user=db_app_auth --password
mysql_config_editor set --login-path=app_reader --host=127.0.0.1 --user=db_app_reader --password
```
*(Enter the passwords defined during `setup_db.py` when prompted).*

## 6. Build and Deploy Containers
Deploy the Streamlit Application and the Zabbix monitoring stack using Docker Compose.

```bash
# Deploy Streamlit
sudo docker build -t food-ai-app:latest -f docker/app/Dockerfile .
sudo docker run -d --name food_ai --restart unless-stopped --network host -v ~/.mylogin.cnf:/root/.mylogin.cnf:ro food-ai-app:latest

# Deploy Zabbix
cd docker/zabbix
sudo bash ../../proper_reset.sh
sudo docker-compose up -d
```

## 7. Verification
- **Streamlit App:** `http://localhost:8501`
- **Zabbix Web UI:** `http://localhost:8080`

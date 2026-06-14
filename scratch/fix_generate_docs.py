import re
import os

file_path = "generate_docs.py"
with open(file_path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

# Replace encoding issues in generate_docs.py header as well
content = content.replace("Lange Franois", "Francois Lange")
content = content.replace("Lange FranA ois", "Francois Lange")

# 1. Find and replace Technical_Document.md .env configuration block
old_tech_env = """    MYSQL_ROOT_PASSWORD=your_db_password_here
    DB_READER_PASS=your_db_password_here
    DB_LOADER_PASS=your_db_password_here
    DB_APP_AUTH_PASS=your_db_password_here
    MYSQL_ZABBIX_PASSWORD=your_db_password_here
    SERVER_HOST=192.168.130.170
    SERVER_USER=francois
    SERVER_PASS=your_db_password_here"""

new_tech_env = """    MYSQL_ROOT_PASSWORD=your_secure_root_password
    DB_READER_PASS=your_secure_reader_password
    DB_LOADER_PASS=your_secure_loader_password
    DB_APP_AUTH_PASS=your_secure_auth_password
    MYSQL_ZABBIX_PASSWORD=your_secure_zabbix_password
    SERVER_HOST=192.168.130.170
    SERVER_USER=francois
    SERVER_PASS=your_secure_server_password
    
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
    TAIGA_PASS=your_taiga_password"""

content = content.replace(old_tech_env, new_tech_env)

# 2. Overwrite Installation_Guide.md content block inside generate_docs.py
old_install_guide_content = """    "Installation_Guide.md": \"\"\"# $Id$
# Installation Guide

## Requirements
- Ubuntu 24.04 LTS (or WSL2)
- Docker & Docker Compose
- 16GB RAM Minimum

## Deployment Steps
1. **Clone the Repository**:
   - *Online Mode*: `git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git`
   - *Offline/Disconnected Mode*: Copy the repository files directly to the target environment via SCP or USB storage.
2. `cd LocalFoodAI_lanfr144`
3. `chmod +x data_sync.sh backup_db.sh`
4. **Deploy Stack**:
   - For regular production: `docker compose up -d --build`
   - For local/offline single-node fallback: `docker compose -f docker-compose_skip.yml up -d`
5. Navigate to `http://localhost` (or `http://localhost:8502` for direct Streamlit port)
\"\"\","""

new_install_guide_content = """    "Installation_Guide.md": \"\"\"# $Id$
# Local Food AI - Detailed Installation and Deployment Guide

This guide describes how to provision the host hypervisor, install Docker on Ubuntu, clone the repository, check out the correct branch, and launch the application.

## 1. WSL2 Ubuntu Instance Setup

To create a dedicated WSL2 environment for the application, execute the following command in an Administrator PowerShell window:
```powershell
wsl --install -d Ubuntu-22.04 --name Dopro1
```

During initialization, configure the default Unix user and password as prompted:
```
Create a default Unix user account: lanfr144
New password:
Retype new password:
passwd: password updated successfully
```

> [!WARNING]
> **WSL Filesystem Mounts**: By default, launching WSL may place you in a Windows filesystem mount (e.g. `/mnt/d/...`). To prevent performance degradation and permission bugs, navigate to your WSL home directory immediately:
```bash
cd ~
```

---

## 2. Docker & Docker Compose Installation inside WSL Ubuntu

To install Docker directly inside your WSL Ubuntu instance (without Docker Desktop):

### Step 2.1: Clean Existing Docker Versions
```bash
sudo apt remove -y docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc
```

### Step 2.2: Add Docker's Official GPG Key & Repository
```bash
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: \\$(. /etc/os-release && echo "\\${UBUNTU_CODENAME:-\\$VERSION_CODENAME}")
Components: stable
Architectures: \\$(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

### Step 2.3: Install Docker Components
```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### Step 2.4: Start and Enable Docker Daemon
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### Step 2.5: Add User to the Docker Group
Ensure you can execute Docker commands without `sudo`:
```bash
grep "^docker:" /etc/group || sudo addgroup docker
sudo usermod -aG docker \\$USER
```

### Step 2.6: Reboot the WSL Instance
Execute the command below inside WSL to gracefully reboot the instance:
```bash
cd /mnt/c/ && cmd.exe /c start "rebooting WSL" cmd /c "timeout 5 && wsl -d \\$WSL_DISTRO_NAME" && wsl.exe --terminate \\$WSL_DISTRO_NAME
```

Upon reconnecting, verify Docker is running by starting the hello-world container:
```bash
docker run hello-world
```

---

## 3. Network Configuration & Performance Tuning

### Step 3.1: Switch to Legacy IPTables
Ubuntu 22.04 uses `nftables` by default. Switch to legacy iptables to ensure Docker network NAT rules match correctly:
```bash
sudo update-alternatives --config iptables
# Select option 1 (iptables-legacy)
```

### Step 3.2: Configure DNS Settings
To ensure reliable package downloads and LLM registry calls:
```bash
echo "1,\\$ s/^/#/
\\$ a
nameserver 1.1.1.1
.
w
q" | sudo ed /etc/resolv.conf

echo "\\$ a
# Added these 2 lines:
[network]
generateResolvConf = false
.
w
q" | sudo ed /etc/wsl.conf
```

---

## 4. Repository Clones & Branch Governance

There are two repositories configured for this project:
- Production Repository: `https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git`
- GitHub Mirror (Clone): `https://github.com/lanfr144/LocalFoodAI_lanfr144`

Clone the primary repository inside your home directory:
```bash
git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git
cd LocalFoodAI_lanfr144
```

### Step 4.1: List Available Branches
Inspect both local and remote branches on the server:
```bash
git branch -a
```
*(Shows available branches like `remotes/origin/main` or `remotes/origin/dev`)*

### Step 4.2: Track and Check Out the Right Branch
Select the main production branch and extract it:
```bash
git checkout main
```
*(If the repository uses a master branch, replace 'main' with 'master')*

### Step 4.3: Set Default Branch (Optional)
To set the default tracking branch for your local copy:
```bash
git remote set-head origin main
```

---

## 5. Launching the App

Ensure the runbooks and sync scripts have executable permissions:
```bash
chmod +x data_sync.sh backup_db.sh manage_services.sh scripts/manage_models.sh
```

Follow the standard runbook to initialize credentials and launch services:
```bash
# 1. Create a local .env file based on step 3 guidelines
# 2. Run the service manager to spin up containers
./manage_services.sh start
```
\"\"\",
"""

content = content.replace(old_install_guide_content, new_install_guide_content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("generate_docs.py successfully updated and encoding sanitized.")

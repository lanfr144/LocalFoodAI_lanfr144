The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:Uninstall_Guide.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Local Food AI - Uninstallation & Teardown Guide

This document outlines the standard uninstallation procedures to completely remove the **Local Food AI** stack components from both Windows hosts and Linux/WSL deployment environments.

---

## 1. Linux & WSL Client Uninstallation

To cleanly purge the containerized services, databases, virtual environments, and log files:

### Step 1.1: Stop & Remove Docker Containers & Volumes
Bring down the Docker Compose stack and permanently delete all associated network interfaces and database volumes:
```bash
# Navigate to the project directory
cd /dossier/du/projet/Food

# Stop services and remove containers, networks, and volumes
./manage_services.sh stop
docker compose down -v
```
*Note: The `-v` flag is critical as it completely purges the MySQL persistent data directories.*

### Step 1.2: Remove Local Project Docker Images
Clean up the built application images from the local Docker cache:
```bash
docker rmi food-app food-ingest
```

### Step 1.3: Clean Up Virtual Environments, Logs & Backups
Delete local administrator logs, backup directories, and Python virtual environment libraries:
```bash
rm -rf .venv/
rm -rf backups/
rm -rf logs/
rm -rf data/
```

### Step 1.4: Purge Docker CE (Optional)
If you wish to completely uninstall Docker CE from the Ubuntu/WSL environment:
```bash
sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
```

---

## 2. Windows Host Uninstallation

To remove all hypervisor and subsystem configurations from the Windows client:

### Step 2.1: Unregister and Delete the WSL Subsystem Environment
To completely wipe the WSL2 Ubuntu environment and its entire virtual hard disk (VHD):
1. Open a PowerShell terminal as Administrator.
2. Execute the unregister command:
```powershell
wsl --unregister Dopro1
```
*Warning: This action is irreversible. All configurations, tools, and code inside the WSL `Dopro1` container will be permanently deleted.*

### Step 2.2: Remove VirtualBox Virtual Machines (if applicable)
If you deployed Ollama or Zabbix nodes on dedicated VirtualBox VMs:
1. Open PowerShell or Command Prompt.
2. Run the VBoxManage tool to remove the VMs:
```cmd
VBoxManage unregistervm "Ollama_Server" --delete
VBoxManage unregistervm "Zabbix_Server" --delete
```

### Step 2.3: Disable Windows Virtualization Features (Optional)
To disable WSL and Virtual Machine Platform features on the Windows host:
```powershell
Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
Disable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
```
*Note: A system reboot is required to complete this step.*

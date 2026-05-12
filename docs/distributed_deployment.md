# Multi-Hypervisor Distributed Deployment (Proof of Concept)

This document provides the exact procedure to decouple the monolithic `docker-compose.yml` into a fully distributed, cross-hypervisor microservice architecture.

## 1. Architectural Topology
To demonstrate cross-platform interoperability, the application stack is split across three distinct virtualized environments on the host machine.

- **VM 1: Hyper-V (Ubuntu Server)**
  - **Container**: `mysql` (Database Engine)
  - **IP Subnet Allocation**: `192.168.130.170` (Bridged)
- **VM 2: VirtualBox (Debian/Ubuntu)**
  - **Container**: `ollama` (Local LLM) + `searxng` (Web Search)
  - **IP Subnet Allocation**: `192.168.130.171` (Bridged)
- **VM 3: WSL2 (Windows Subsystem for Linux)**
  - **Container**: `app` (Streamlit Web Interface)
  - **IP Subnet Allocation**: `192.168.130.172` (NAT/Bridged via Hyper-V switch)

## 2. Networking Configuration
To ensure these isolated VMs can communicate, you must configure a **Bridged Virtual Switch**:
1. Open Hyper-V Virtual Switch Manager.
2. Create an "External" switch mapped to your physical network adapter.
3. Attach VM 1 (Hyper-V) and VM 3 (WSL2) to this switch.
4. In VirtualBox, set the Network Adapter for VM 2 to "Bridged Adapter" pointing to the same physical interface.
5. Disable `ufw` or Windows Firewall for the `192.168.130.0/24` subnet on all hosts.

## 3. Deployment Steps

### Step 1: Deploy Database on Hyper-V
On VM 1, create a `docker-compose.yml` containing *only* the MySQL service.
```yaml
services:
  mysql:
    build:
      context: ./docker/mysql
    ports:
      - "3306:3306"
      - "161:161/udp" # Expose SNMP
    volumes:
      - mysql_data:/var/lib/mysql
```

### Step 2: Deploy AI Engines on VirtualBox
On VM 2, create a `docker-compose.yml` containing the AI services.
```yaml
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
      - "161:161/udp" # Requires sidecar or custom image for SNMP
  searxng:
    image: searxng/searxng:latest
    ports:
      - "8080:8080"
```

### Step 3: Deploy Frontend on WSL2
On VM 3, configure the App container to point to the external IP addresses rather than Docker DNS hostnames.
Update your `.env` file on WSL2:
```ini
DB_HOST=192.168.130.170
OLLAMA_HOST=http://192.168.130.171:11434
SEARXNG_HOST=http://192.168.130.171:8080
```

## 4. SNMP Telemetry within Containers
By default, Docker containers run a single process (PID 1). To run `snmpd` alongside the application in *every* container, we use `supervisord`.

**Example Dockerfile Modification for App Container:**
```dockerfile
RUN apt-get update && apt-get install -y supervisor snmpd
COPY snmpd.conf /etc/snmp/snmpd.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 8501 161/udp
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
```

**supervisord.conf:**
```ini
[supervisord]
nodaemon=true

[program:app]
command=streamlit run app.py
autorestart=true

[program:snmpd]
command=/usr/sbin/snmpd -f
autorestart=true
```

## 5. Zabbix Monitoring Integration
1. On the Zabbix Server (`192.168.130.170:8081`), navigate to **Configuration > Hosts**.
2. Add three separate Hosts corresponding to the VM IPs (`192.168.130.170`, `192.168.130.171`, `192.168.130.172`).
3. Attach the "Linux SNMP" template to each host. Zabbix will now automatically poll CPU, RAM, and Disk I/O natively from within each Docker container across the distributed environment.

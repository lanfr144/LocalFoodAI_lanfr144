# $Id$
# Installation Guide

## Requirements
- Ubuntu 24.04 LTS (or WSL2)
- Docker & Docker Compose
- 16GB RAM Minimum

## Deployment Steps
1. `git clone https://git.btshub.lu/lanfr/LocalFoodAI_lanfr144.git`
2. `cd LocalFoodAI_lanfr144`
3. `chmod +x data_sync.sh backup_db.sh`
4. `docker-compose up -d --build`
5. Navigate to `http://<server-ip>`

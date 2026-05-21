# $Id$ log fields, date format, and redesign architecture.md diagram [v1.0.2] $
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

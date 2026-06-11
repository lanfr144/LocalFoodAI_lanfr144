# $Id: 03cbc893f143c3ae43fc35e97913bedb89b41e23 Lange François lanfr144@school.lu 2026/06/11 10:38:26 Lange François lanfr144@school.lu 2026/06/11 10:38:26   [#1] chore: fix git-ident-filter self-modification regex bug by concatenating search strings [PreRelease-1.0-28-g03cbc89] $
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

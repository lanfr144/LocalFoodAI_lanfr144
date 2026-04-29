# Installation & Deployment Guide

This guide details how to deploy the Local Food AI stack on an Ubuntu 24.04 server.

## 1. Prerequisites
- Ubuntu 24.04 (e.g., VM at `192.168.130.170`).
- Git, curl.

## 2. Setting Up MySQL
1. Install MySQL Server: `sudo apt install mysql-server`
2. Run `setup_db.py` to construct the schemas.
3. Configure `mysql_config_editor` to store encrypted login paths for `app_auth` and `app_reader`.
   ```bash
   mysql_config_editor set --login-path=app_reader --host=127.0.0.1 --user=db_reader --password
   mysql_config_editor set --login-path=app_auth --host=127.0.0.1 --user=db_auth --password
   ```

## 3. Setting Up Ollama (Local LLM)
The application requires `ollama` to run the Mistral model locally for strict privacy.
1. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. Pull the model: `ollama run mistral`

## 4. Python Environment
1. Clone the repository: `git clone https://git.btshub.lu/...`
2. Setup venv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt (streamlit, pandas, pymysql, bcrypt, ollama)
   ```

## 5. Running the Application
To run the Streamlit frontend:
```bash
streamlit run app.py --server.address 0.0.0.0
```

*Note: If you run this locally on Windows without `mysql_config_editor` paths, you will receive a connection warning.*

## 6. Docker & Kubernetes (Optional)
This repository also contains a full containerized CI/CD suite. 
Navigate to `k8s/` and run `kubectl apply -f .` to spin up the MySQL, Taiga Sync, Ingestion Jobs, and Streamlit App in a resilient cluster.

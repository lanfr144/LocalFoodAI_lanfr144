#!/bin/bash
# -----------------------------------------------------------------------------
# Naked Environment Deployment Script for Ubuntu 24.04
# Run this script to seamlessly fully provision the server for the AI Web App.
# -----------------------------------------------------------------------------

set -e

echo "=========================================================="
echo " Starting Full Environment Deployment for Ubuntu 24.04..."
echo "=========================================================="

# 1. Update system packages
echo ""
echo "[1/6] Updating APT cache and installing system dependencies (GCC, Python, MySQL Server)..."
sudo apt update
sudo apt install -y build-essential gcc python3-venv python3-dev python3-pip curl mysql-server

# 2. Install Ollama natively
echo ""
echo "[2/6] Installing Ollama Engine..."
curl -fsSL https://ollama.com/install.sh | sh

# 3. Secure and setup MySQL Server configuration
echo ""
echo "[3/6] Configuring MySQL Server settings (Local infile & validation policies)..."
# We inject the provided my.cnf configuration directly into the MySQL system config
if [ -f "./my.cnf" ]; then
    sudo cp ./my.cnf /etc/mysql/conf.d/custom_ai_app.cnf
    echo "Custom MySQL configurations applied from my.cnf."
else
    echo "Warning: my.cnf not found in the current directory."
fi

sudo systemctl restart mysql
echo "MySQL Service restarted."

# 4. Set up Python Virtual Environment (PEP 668 compliant)
echo ""
echo "[4/6] Setting up Python 3 Virtual Environment ('venv')..."
python3 -m venv venv
# From here on, we temporarily export the paths to use the new virtual env directly
export PATH="$PWD/venv/bin:$PATH"

# 5. Install Required Python Libraries
echo ""
echo "[5/6] Installing Python dependencies via pip inside venv..."
pip install --upgrade pip
pip install pandas pymysql myloginpath streamlit ollama bcrypt

echo ""
echo "=========================================================="
echo " 🎉 Environment Deployment Complete! "
echo "=========================================================="
echo ""
echo "Next steps:"
echo "1. Activate your virtual environment manually:  source venv/bin/activate"
echo "2. Check your config.ini file details."
echo "3. Run your setup script to configure database users:  python setup_db.py"

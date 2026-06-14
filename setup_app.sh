#!/bin/bash
#ident "@(#)$Format:LocalFoodAI:setup_app.sh:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$""
# ==============================================================================
# Local Food AI - WSL Application Setup Script
# Run inside the WSL Ubuntu environment
# ==============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO] - $1${NC}"
}

log_success() {
    echo -e "${GREEN}[SUCCESS] - $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}[WARNING] - $1${NC}"
}

log_error() {
    echo -e "${RED}[ERROR] - $1${NC}"
}

# 1. Check if running inside WSL
if ! grep -qi "microsoft" /proc/sys/kernel/osrelease 2>/dev/null && ! grep -qi "wsl" /proc/sys/kernel/osrelease 2>/dev/null; then
    log_warn "This script is optimized for WSL. Continuing anyway..."
fi

# 2. Navigate to WSL home directory if run from Windows mount to prevent permission bugs
if [[ "$PWD" == /mnt/* ]]; then
    log_warn "You are running this script from a Windows filesystem mount ($PWD)."
    log_info "Redirecting to your Unix home directory (~)..."
    cd ~
fi

# 3. Clean existing Docker installations
log_info "Step 1/6: Checking and removing old Docker packages..."
sudo apt remove -y docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc || true

# 4. Install Docker dependencies & Repository
log_info "Step 2/6: Setting up Docker repository..."
sudo apt update
sudo apt install -y ca-certificates curl ed
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

# 5. Install Docker CE
log_info "Step 3/6: Installing Docker CE and plugins..."
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 6. Switch IP Tables to Legacy for WSL Docker bridging
log_info "Step 4/6: Switching iptables configuration to legacy..."
# Choose option 1 (iptables-legacy) automatically using update-alternatives
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy

# 7. Update DNS and WSL network configurations
log_info "Step 5/6: Configuring resolv.conf and wsl.conf for stable DNS..."
# Modify resolv.conf to use Cloudflare DNS
echo "1,\$ s/^/#/
\$ a
nameserver 1.1.1.1
.
w
q" | sudo ed /etc/resolv.conf

# Modify wsl.conf to prevent overwrite
echo "\$ a
# Added these 2 lines:
[network]
generateResolvConf = false
.
w
q" | sudo ed /etc/wsl.conf

# 8. User group configuration
log_info "Step 6/6: Configuring Docker group permissions..."
grep "^docker:" /etc/group || sudo addgroup docker
sudo usermod -aG docker "$USER"

log_success "Application Environment Setup Complete!"
log_info "Please reboot your WSL instance to apply changes."
log_info "To reboot WSL, execute this command:"
log_info "cd /mnt/c/ && cmd.exe /c start \"rebooting WSL\" cmd /c \"timeout 5 && wsl -d \$WSL_DISTRO_NAME\" && wsl.exe --terminate \$WSL_DISTRO_NAME"

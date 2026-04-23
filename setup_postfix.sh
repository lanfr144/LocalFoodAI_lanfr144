#!/bin/bash
# run this as root/sudo on the Ubuntu VM to configure SMTP for password resets

echo "🔧 Installing and Configuring Postfix for Local Food AI..."

sudo apt-get update
# Non-interactive installation of postfix configured for local delivery
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y postfix

echo "🔒 Disabling external relay to maintain 100% Privacy-First Architecture..."
# Ensure postfix only listens to localhost for security
sudo postconf -e "inet_interfaces = loopback-only"
sudo postconf -e "mydestination = localhost.localdomain, localhost"

echo "🔄 Restarting Mail Service..."
sudo systemctl restart postfix
sudo systemctl enable postfix

echo "✅ Success! The 'Forgot Password' feature in the Streamlit UI will now officially route emails to users via the internal Ubuntu backbone!"

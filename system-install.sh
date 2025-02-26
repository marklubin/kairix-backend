#!/bin/bash

set -e  # Exit script on error

echo "🚀 Kairix System Dependency Check & Installation"

# Function to check if a command exists
check_command() {
    command -v "$1" &> /dev/null
}

# Function to install a package if it's missing
install_package() {
    if ! check_command "$1"; then
        echo "🔧 Installing $1..."
        sudo apt install -y "$2"
    else
        echo "✅ $1 is already installed."
    fi
}

# Update system
echo "🔄 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Verify Python installation
if ! check_command python3; then
    echo "🐍 Installing Python..."
    sudo apt install -y python3 python3-pip
else
    echo "✅ Python installed: $(python3 --version)"
fi

# Verify Git installation
install_package "git" "git"

# Verify Poetry installation
if ! check_command poetry; then
    echo "📦 Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
else
    echo "✅ Poetry installed: $(poetry --version)"
fi

# Verify system dependencies
install_package "curl" "curl"
install_package "unzip" "unzip"
install_package "wget" "wget"

# Verify Gunicorn (if using for production)
if ! check_command gunicorn; then
    echo "🐍 Installing Gunicorn..."
    poetry add gunicorn
else
    echo "✅ Gunicorn installed."
fi

# Verify Nginx (for reverse proxy)
install_package "nginx" "nginx"

# Verify firewall rules for Flask (port 5000)
if sudo ufw status | grep -q "5000"; then
    echo "✅ Port 5000 is open."
else
    echo "🔓 Opening port 5000 for Flask..."
    sudo ufw allow 5000/tcp
fi

# Check if systemd service exists for Kairix
if [ -f /etc/systemd/system/kairix.service ]; then
    echo "✅ Kairix systemd service found."
else
    echo "⚠️ Kairix systemd service not found. You may need to create one."
fi

# Display final system status
echo "🎯 System Dependency Check Completed Successfully!"
echo "🚀 You can now deploy Kairix backend."

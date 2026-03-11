#!/bin/bash
set -euo pipefail

apt-get update
apt-get install -y curl ripgrep

# Install Pochi

echo "downloading latest pochi"
curl -fsSL https://getpochi.com/install.sh | bash


ln -s ~/.pochi/bin/pochi /usr/local/bin/pochi
mkdir -p /logs/agent/pochi

pochi --version
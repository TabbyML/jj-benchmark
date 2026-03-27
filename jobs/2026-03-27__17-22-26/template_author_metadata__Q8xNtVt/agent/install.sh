#!/bin/bash
set -euo pipefail

apt-get update
apt-get install -y curl ripgrep

# Install Pochi

echo "downloading pochi version: v0.6.5"
curl -fsSL https://getpochi.com/install.sh | bash -s "pochi-v0.6.5"


ln -s ~/.pochi/bin/pochi /usr/local/bin/pochi
mkdir -p /logs/agent/pochi

pochi --version
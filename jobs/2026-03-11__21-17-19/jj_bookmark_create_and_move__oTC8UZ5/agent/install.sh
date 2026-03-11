#!/bin/bash
set -euo pipefail

apt-get update
apt-get install -y curl ripgrep

# Install Pochi

echo "downloading latest pochi"
curl -fsSL https://getpochi.com/install.sh | bash
# mkdir -p ~/.pochi/bin
# curl -fsSL "https://github.com/TabbyML/pochi/releases/download/cli@0.5.105/pochi-linux-x64.tar.gz" | tar -xz -C ~/.pochi/bin


ln -s ~/.pochi/bin/pochi /usr/local/bin/pochi
mkdir -p /logs/agent/pochi

pochi --version
FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest python3-requests bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm i -g @wasp.sh/wasp-cli@latest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Wasp development environment with Node.js 24.x and Wasp CLI for building full-stack applications."

# Container contents:
# 1. For development:
#   - Node.js 24.x and npm
#   - Wasp CLI (@wasp.sh/wasp-cli) for full-stack application development
#   - Git for project initialization and version control
# 2. For automated verification:
#   - Python 3, pip, pytest, and requests for running verification scripts
#   - curl for network and API endpoint checks

CMD ["/bin/bash"]

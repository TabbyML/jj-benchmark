FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash sqlite3 && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g @wasp.sh/wasp-cli@latest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Wasp development environment with Node.js 24.x for customizing signup fields task."

# Container contents:
# 1. For development:
#   - Node.js 24.x and npm
#   - Wasp CLI (@wasp.sh/wasp-cli)
#   - Git for project initialization
#   - sqlite3 for database inspection
# 2. For automated verification:
#   - Python 3, pip, and pytest
#   - curl for network checks

CMD ["/bin/bash"]

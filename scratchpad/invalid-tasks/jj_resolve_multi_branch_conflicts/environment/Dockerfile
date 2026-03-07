FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: resolve conflicts across multiple files in a multi-branch merge"

ENV DEBIAN_FRONTEND=noninteractive
ENV EDITOR=true
ENV JJ_USER="Test User"
ENV JJ_EMAIL="test@example.com"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Install jj from official release
RUN curl -fsSL \
    https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

# Create home directory
RUN mkdir -p /home/user && chmod 0755 /home/user

WORKDIR /home/user

# Initialise the jj repository
RUN mkdir -p /home/user/workspace/src \
    && cd /home/user/workspace \
    && jj git init --no-colocate . \
    && jj config set --repo user.name "Test User" \
    && jj config set --repo user.email "test@example.com"

# Commit 1: base / main
RUN cd /home/user/workspace \
    && printf '# Web service configuration\nHOST = "localhost"\nPORT = 8080\nLOG_LEVEL = "INFO"\nDEBUG = False\n' > src/server.py \
    && printf '# HTTP route definitions\nroutes = [\n    {"path": "/", "handler": "index", "description": "Home page"},\n    {"path": "/health", "handler": "health_check", "description": "Health endpoint"},\n]\n' > src/routes.py \
    && jj describe -m "base: initial web service setup" \
    && jj bookmark create main -r @

# Commit 2: feature-api — changes HOST and PORT in server.py, updates "/" description and adds /api/v2/users in routes.py
RUN cd /home/user/workspace \
    && jj new main \
    && printf '# Web service configuration\nHOST = "api.example.com"\nPORT = 9000\nLOG_LEVEL = "INFO"\nDEBUG = False\n' > src/server.py \
    && printf '# HTTP route definitions\nroutes = [\n    {"path": "/", "handler": "index", "description": "Home page (api-v2)"},\n    {"path": "/health", "handler": "health_check", "description": "Health endpoint"},\n    {"path": "/api/v2/users", "handler": "users_v2", "description": "Users API v2"},\n]\n' > src/routes.py \
    && jj describe -m "api-v2: set HOST to api.example.com, bump port, add users v2 route" \
    && jj bookmark create feature-api -r @

# Commit 3: feature-logging — changes HOST and LOG_LEVEL in server.py, updates "/" description in routes.py
RUN cd /home/user/workspace \
    && jj new main \
    && printf '# Web service configuration\nHOST = "0.0.0.0"\nPORT = 8080\nLOG_LEVEL = "WARNING"\nDEBUG = False\n' > src/server.py \
    && printf '# HTTP route definitions\nroutes = [\n    {"path": "/", "handler": "index", "description": "Home page (v2)"},\n    {"path": "/health", "handler": "health_check", "description": "Health endpoint"},\n]\n' > src/routes.py \
    && jj describe -m "logging-update: listen on all interfaces and raise log level to WARNING" \
    && jj bookmark create feature-logging -r @

# Create merge commit — produces conflicts in both src/server.py and src/routes.py
RUN cd /home/user/workspace \
    && jj new feature-api feature-logging; true

CMD ["/bin/bash"]

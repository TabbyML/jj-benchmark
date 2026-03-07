FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    jj git init --no-colocate . && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "# Project README" > README.md && \
    jj describe -m "initial commit" && \
    jj new && \
    mkdir -p src && \
    touch src/__init__.py && \
    echo '[database]\nhost = "localhost"\nport = 5432\nname = "appdb"\n' > config.toml && \
    jj describe -m "add config file" && \
    jj new && \
    printf 'def authenticate(username, password):\n    """Authenticate a user with username and password."""\n    if not username or not password:\n        return False\n    # TODO: integrate with real user store\n    return username == "admin" and password == "secret"\n\n\ndef get_current_user(token):\n    """Return the current user based on auth token."""\n    return None\n' > src/auth.py && \
    jj describe -m "add user authentication module" && \
    AUTH_CHANGE_ID=$(jj log --no-graph -T "change_id" -r "@" | head -1) && \
    jj new && \
    jj abandon "$AUTH_CHANGE_ID"

CMD ["/bin/bash"]

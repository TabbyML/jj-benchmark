FROM ubuntu:22.04

LABEL Author="jj-task-builder"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN curl -fsSL \
    https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

ENV HOME=/home/user
ENV EDITOR=true

# Set up jj user config
RUN mkdir -p /home/user/.config/jj && \
    cat > /home/user/.config/jj/config.toml <<'EOF'
[user]
name = "CI Engineer"
email = "ci@example.com"

[ui]
default-command = "log"
EOF

ENV JJ_CONFIG=/home/user/.config/jj/config.toml

# Create bare git repos to simulate remotes
RUN mkdir -p /home/user/remotes && \
    git init --bare /home/user/remotes/origin.git && \
    git init --bare /home/user/remotes/upstream.git

# Populate upstream bare repo with an "integration" branch
RUN git clone /home/user/remotes/upstream.git /home/user/remotes/_upstream_temp && \
    cd /home/user/remotes/_upstream_temp && \
    git config user.email "ci@example.com" && \
    git config user.name "CI Engineer" && \
    echo "# Integration Pipeline" > pipeline.md && \
    git add pipeline.md && \
    git commit -m "ci: add integration pipeline" && \
    git branch -M integration && \
    git push origin integration && \
    cd /home/user && \
    rm -rf /home/user/remotes/_upstream_temp

# Initialize the main jj repo
RUN mkdir -p /home/user/myrepo && \
    cd /home/user/myrepo && \
    jj git init --no-colocate . && \
    jj config set --repo user.name "CI Engineer" && \
    jj config set --repo user.email "ci@example.com"

# Create commit history
RUN cd /home/user/myrepo && \
    mkdir -p src && \
    echo "# My Project" > README.md && \
    echo "print('hello')" > src/main.py && \
    jj describe -m "init: project scaffold" && \
    jj new

RUN cd /home/user/myrepo && \
    echo "# Release Notes" > RELEASE.md && \
    echo "v1.0 - initial release" >> RELEASE.md && \
    jj describe -m "feat: add release notes" && \
    jj new

# Add remotes to the jj repo
RUN cd /home/user/myrepo && \
    jj git remote add origin /home/user/remotes/origin.git && \
    jj git remote add upstream /home/user/remotes/upstream.git

CMD ["/bin/bash"]

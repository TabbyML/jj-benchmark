FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: set alias st=status and ui.paginate=never in user config"

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && pip3 install --no-cache-dir pytest \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Set up user identity config
RUN mkdir -p /home/user/.config/jj && \
    printf '[user]\nname = "Dev User"\nemail = "dev@example.com"\n' \
    > /home/user/.config/jj/config.toml

# Create the jj repository at /home/user/myrepo with one commit
RUN mkdir -p /home/user/myrepo && \
    cd /home/user/myrepo && \
    HOME=/home/user jj git init --quiet && \
    HOME=/home/user jj config set --repo user.name "Dev User" && \
    HOME=/home/user jj config set --repo user.email "dev@example.com" && \
    echo "hello world" > README.md && \
    HOME=/home/user EDITOR=true jj describe -m "initial commit" && \
    HOME=/home/user EDITOR=true jj new

# Container contents:
# - /home/user/.config/jj/config.toml  (user config with identity, no aliases, no ui.paginate)
# - /home/user/myrepo/                  (jj repository with one commit "initial commit")
# - /home/user/myrepo/.jj/              (jj internals)
# - /home/user/myrepo/README.md         (tracked file)

CMD ["/bin/bash"]

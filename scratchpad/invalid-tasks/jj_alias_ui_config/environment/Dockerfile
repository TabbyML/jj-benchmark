FROM ubuntu:22.04

# Task: jj_alias_ui_config
# Category: set and debug alias and ui config options
# Scenario: new teammate onboarding to jj
# Description: Sets up a jj git repo at /home/user/myrepo with a minimal user
#              config (no aliases). The user must configure identity, aliases,
#              and UI settings via jj config set --user commands.

LABEL task="jj_alias_ui_config"
LABEL category="set and debug alias and ui config options"

ENV DEBIAN_FRONTEND=noninteractive
ENV EDITOR=true

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && pip3 install pytest \
    && rm -rf /var/lib/apt/lists/*

# Install jj from official release
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

# Create the home user directory
RUN mkdir -p /home/user

# Set up the jj config directory with a minimal config (no aliases yet)
RUN mkdir -p /home/user/.config/jj && \
    printf '[user]\nname = "User"\nemail = "user@localhost"\n' \
    > /home/user/.config/jj/config.toml

# Initialize the jj git repository
RUN mkdir -p /home/user/myrepo && \
    cd /home/user/myrepo && \
    HOME=/home/user jj git init --colocate

# Create a README and make an initial commit
RUN cd /home/user/myrepo && \
    echo "# My Repo" > README.md && \
    HOME=/home/user jj describe -m "initial commit" && \
    HOME=/home/user jj new

CMD ["/bin/bash"]

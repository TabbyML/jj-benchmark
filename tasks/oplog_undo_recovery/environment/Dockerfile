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

# Install jj from official release
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Configure jj user identity
ENV JJ_USER="Support Engineer"
ENV JJ_EMAIL="support@example.com"
ENV EDITOR=true

# Initialize the jj repo and build commit history
RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    jj git init --no-colocate .

# Commit 1: add initial readme
RUN cd /home/user/project && \
    echo "# My Project" > README.md && \
    jj describe -m "add initial readme" && \
    jj new

# Commit 2: implement core feature
RUN cd /home/user/project && \
    printf 'def core_feature():\n    return "core feature implementation"\n' > core.py && \
    jj describe -m "implement core feature" && \
    jj new

# Commit 3: add tests for core feature
RUN cd /home/user/project && \
    printf 'from core import core_feature\n\ndef test_core_feature():\n    assert core_feature() == "core feature implementation"\n' > tests.py && \
    jj describe -m "add tests for core feature" && \
    jj new

# Mistake 1: Re-describe the "implement core feature" commit with a bad message
RUN cd /home/user/project && \
    jj describe -m "WIP: bad description do not merge" \
        -r "description(substring:'implement core feature')"

# Mistake 2: Abandon the "add tests for core feature" commit
RUN cd /home/user/project && \
    jj abandon "description(substring:'add tests for core feature')"

CMD ["/bin/bash"]

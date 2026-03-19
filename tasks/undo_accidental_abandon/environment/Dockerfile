FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: undo accidental abandon — support engineer recovers lost commit via operation log"

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

# Install jj from upstream release
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

# Configure git identity (required by jj)
RUN git config --global user.name "Support Engineer" && \
    git config --global user.email "support@example.com"

ENV EDITOR=true

# Bootstrap the repository
RUN mkdir -p /home/user/project

RUN jj git init /home/user/project

RUN jj --repository /home/user/project config set --repo user.name "Support Engineer" && \
    jj --repository /home/user/project config set --repo user.email "support@example.com"

# Commit 1: initial project scaffold
RUN mkdir -p /home/user/project/src && \
    echo "# MyProject" > /home/user/project/README.md && \
    jj --repository /home/user/project describe -m "initial project scaffold" && \
    jj --repository /home/user/project new

# Commit 2: add user authentication module
RUN echo "# Authentication module" > /home/user/project/src/auth.py && \
    jj --repository /home/user/project describe -m "add user authentication module" && \
    jj --repository /home/user/project new

# Commit 3: update README with usage instructions
RUN printf "# MyProject\n\n## Usage\nSee docs." > /home/user/project/README.md && \
    jj --repository /home/user/project describe -m "update README with usage instructions"

# Create the 'main' bookmark pointing to this commit
RUN jj --repository /home/user/project bookmark create main -r '@'

# Start a new empty working copy on top
RUN jj --repository /home/user/project new

# Simulate the accidental abandon of "add user authentication module"
RUN jj --repository /home/user/project abandon 'description(substring:"add user authentication module")'

WORKDIR /home/user/project

CMD ["/bin/bash"]

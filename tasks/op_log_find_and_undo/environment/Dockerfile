FROM ubuntu:22.04

# Task: jj_op_log_find_and_undo
# Category: inspect operation log and recover with undo
# Complexity: simple set of 3-4 commands
# Scenario: support engineer recovering lost work
# Description: Bootstrap a jj repo where the 'feature' bookmark and its commit
#              were accidentally abandoned. The user must inspect jj op log and
#              run jj undo to recover the lost work.

LABEL author="jj-task-builder"
LABEL description="jj task: inspect op log and recover lost work with jj undo"

ENV DEBIAN_FRONTEND=noninteractive
ENV EDITOR=true

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pytest

# Install jj from upstream release (x86_64 Linux musl binary)
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj \
    && chmod +x /usr/local/bin/jj

# Set up /home/user
RUN mkdir -p /home/user && chmod 0755 /home/user

# Configure git identity globally (required by jj)
RUN git config --global user.name "Support Engineer" && \
    git config --global user.email "support@example.com"

# Initialize the jj-backed git repository
RUN jj git init /home/user/project

# Set repo-level identity
RUN jj --repository /home/user/project config set --repo user.name "Support Engineer" && \
    jj --repository /home/user/project config set --repo user.email "support@example.com"

# Commit 1: initial project setup
RUN echo "# MyProject" > /home/user/project/README.md && \
    jj --repository /home/user/project describe -m "initial project setup" && \
    jj --repository /home/user/project new

# Commit 2: implement feature (this will be abandoned to simulate the accident)
RUN echo "feature work" > /home/user/project/feature.txt && \
    jj --repository /home/user/project describe -m "implement feature"

# Create the 'feature' bookmark pointing to the "implement feature" commit
RUN jj --repository /home/user/project bookmark create feature -r '@'

# Move working copy forward
RUN jj --repository /home/user/project new

# Commit 3: a follow-up commit on the main line
RUN echo "# Main work" > /home/user/project/main.txt && \
    jj --repository /home/user/project describe -m "main follow-up work" && \
    jj --repository /home/user/project new

# Simulate the accident: abandon the 'feature' commit
# This removes "implement feature" from visible history and deletes the 'feature' bookmark
RUN jj --repository /home/user/project abandon 'feature'

WORKDIR /home/user/project

CMD ["/bin/bash"]

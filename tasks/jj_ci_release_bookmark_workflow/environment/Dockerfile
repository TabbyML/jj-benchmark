# Dockerfile for jj_ci_release_bookmark_workflow
#
# Task: CI Release Bookmark Workflow
# Scenario: build/release engineer maintaining CI
# Category: create reproducible CI-friendly tasks with jj
#
# Installs jj v0.38.0 and sets up a project with three stacked feature commits
# that the user must squash, tag, and bookmark to create a v1.0 release.

FROM ubuntu:22.04

LABEL task="jj_ci_release_bookmark_workflow"
LABEL description="CI release bookmark workflow task for jj"

ENV DEBIAN_FRONTEND=noninteractive

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
RUN pip3 install pytest

# Install jj v0.38.0
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

# Create user home directory
RUN mkdir -p /home/user

# Set environment
ENV HOME=/home/user
ENV EDITOR=true
ENV JJ_NO_PAGER=1
ENV PAGER=cat

# Bootstrap: set up the jj repository with three stacked feature commits
RUN jj git init /home/user/project

WORKDIR /home/user/project

# Configure user identity at repo level
RUN jj config set --repo user.name "CI Bot" && \
    jj config set --repo user.email "ci@example.com"

# Add .gitignore
RUN echo "*.pyc\n__pycache__/\n.lesshst" > .gitignore && \
    jj file track .gitignore

# Commit 1: feat: add authentication module
RUN mkdir -p src && \
    echo "# Authentication module" > src/auth.py && \
    jj file track src/auth.py && \
    jj describe -m "feat: add authentication module" && \
    jj new

# Commit 2: feat: add payment processing
RUN echo "# Payment processing module" > src/payment.py && \
    jj file track src/payment.py && \
    jj describe -m "feat: add payment processing" && \
    jj new

# Commit 3: feat: add notification service
RUN echo "# Notification service module" > src/notify.py && \
    jj file track src/notify.py && \
    jj describe -m "feat: add notification service" && \
    jj new

# Verify initial state
RUN jj log --no-graph -r 'mutable() & ~@ & ~root()' -T 'description ++ "\n"'

CMD ["/bin/bash"]

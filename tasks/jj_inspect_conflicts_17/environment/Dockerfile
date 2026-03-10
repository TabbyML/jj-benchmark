FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo with a conflict in config.yaml between main and feature branches."

RUN jj git init /home/user/project-alpha && \
    cd /home/user/project-alpha && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    cat << 'EOF' > config.yaml
version: 1.0
EOF
    
RUN cd /home/user/project-alpha && \
    jj describe -m "base: initial config" && \
    jj bookmark create main -r @ && \
    jj new main -m "main: set environment to production" && \
    cat << 'EOF' > config.yaml
version: 1.0
environment: production
EOF

RUN cd /home/user/project-alpha && \
    jj bookmark set main -r @ && \
    jj new main- -m "feature: enable feature flag" && \
    cat << 'EOF' > config.yaml
version: 1.0
feature_flag: enabled
EOF

RUN cd /home/user/project-alpha && \
    jj bookmark create feature -r @ && \
    jj new main feature -m "merge: main and feature"

# Container contents:
#   - /home/user/project-alpha — jj repository with a conflict in config.yaml:
#       - "base: initial config"
#       - "main: set environment to production"
#       - "feature: enable feature flag"
#       - "merge: main and feature" (conflicted commit)
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]

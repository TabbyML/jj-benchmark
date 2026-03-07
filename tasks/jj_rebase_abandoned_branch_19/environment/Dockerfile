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
LABEL Description="jj repo with an abandoned feature-x branch that needs recovery and rebasing"

RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj git init && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "main content" > file.txt && \
    jj describe -m "Initial commit" && \
    jj bookmark create main && \
    jj new main -m "Update main" && \
    echo "main update" >> file.txt && \
    jj bookmark move main && \
    jj new main -m "feature-x work" && \
    echo "feature-x content" > feature.txt && \
    jj bookmark create feature-x && \
    jj new main -m "Another main update" && \
    echo "another update" >> file.txt && \
    jj bookmark move main && \
    jj abandon feature-x

# Container contents:
#   - /home/user/repo - jj repository with main branch and an abandoned hidden commit previously pointed to by feature-x.
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]

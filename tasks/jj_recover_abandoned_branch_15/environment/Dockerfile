FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.34.0/jj-v0.34.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo with an abandoned commit containing login page work."

RUN jj git init /home/user/myrepo && \
    cd /home/user/myrepo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "initial main content" > file.txt && \
    jj describe -m "Initial commit" && \
    jj bookmark create main && \
    jj new -m "feat: implement login page" && \
    echo "login page content" > login.txt && \
    jj bookmark create feature-login && \
    jj abandon

# Container contents:
#   - /home/user/myrepo  — jj repository with:
#       - "Initial commit" on main
#       - An abandoned commit "feat: implement login page" that was previously on feature-login
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]

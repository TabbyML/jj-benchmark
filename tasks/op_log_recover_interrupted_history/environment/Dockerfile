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
LABEL Description="jj repo with an interrupted rebase operation in /home/user/repo."

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "base" > base.txt && \
    jj new -m "Add base file" && \
    echo "login 1" > login.txt && \
    jj new -m "Start feature-login" && \
    echo "login 2" >> login.txt && \
    jj describe -m "Finish feature-login" && \
    jj bookmark create feature-login && \
    jj new "root()" -m "Another feature" && \
    echo "other" > other.txt && \
    jj rebase -b feature-login -d @

# Container contents:
#   - /home/user/repo — jj repository with a base commit, two feature commits, and another feature branch.
#   - The feature-login bookmark was rebased onto another branch to simulate an interrupted operation.
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]
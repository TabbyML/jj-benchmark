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
LABEL Description="jj repo with linear audit history and WIP commits to prune."

RUN jj git init /home/user/audit-repo && \
    cd /home/user/audit-repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    echo "entry 1" > entry1.txt && \
    jj describe -m "Audit log entry 1" && \
    jj new && \
    echo "entry 2" > entry2.txt && \
    jj describe -m "Audit log entry 2" && \
    jj new && \
    echo "entry 3" > entry3.txt && \
    jj describe -m "Audit log entry 3" && \
    jj bookmark create main -r @ && \
    jj new && \
    echo "wip 1" > wip1.txt && \
    jj describe -m "WIP: data ingest part 1" && \
    jj new && \
    echo "wip 2" > wip2.txt && \
    jj describe -m "WIP: data ingest part 2" && \
    jj edit main

# Container contents:
#   - /home/user/audit-repo  — jj repository with linear history and WIP commits:
#       - "Audit log entry 1"
#       - "Audit log entry 2"
#       - "Audit log entry 3" (bookmarked as main, current working copy)
#       - "WIP: data ingest part 1"
#       - "WIP: data ingest part 2"
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]

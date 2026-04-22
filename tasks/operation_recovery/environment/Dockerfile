FROM ubuntu:24.04

RUN apt-get update && apt-get install -y curl git python3 python3-pip && \
    curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Environment with multiple operations."

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    git init && \
    jj git init --colocate && \
    jj config set --user user.name "Alice" && \
    jj config set --user user.email "alice@example.com" && \
    echo "C1" > file1.txt && jj commit -m "Commit 1" && \
    echo "C2" > file2.txt && jj commit -m "Commit 2" && \
    echo "C3" > file3.txt && jj commit -m "Commit 3" && \
    echo "C4" > file4.txt && jj commit -m "Commit 4" && \
    echo "C5" > file5.txt && jj commit -m "Commit 5"

# Container contents:
#   - jj installed
#   - /home/user/project with 5 commits

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
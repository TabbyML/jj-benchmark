FROM ubuntu:24.04

RUN apt-get update && apt-get install -y curl git python3 python3-pip && \
    curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Environment with a combined commit."

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    git init && \
    jj git init --colocate && \
    jj config set --user user.name "Alice" && \
    jj config set --user user.email "alice@example.com" && \
    echo "Base A" > fileA.txt && echo "Base B" > fileB.txt && jj commit -m "Base commit" && \
    echo "Mod A" > fileA.txt && echo "Mod B" > fileB.txt && jj commit -m "Combined changes"

# Container contents:
#   - jj installed
#   - /home/user/project with a combined commit modifying fileA.txt and fileB.txt

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL \
    https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Jujutsu repository with a stack of commits to edit."

RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    jj git init --colocate && \
    jj describe -m "Add file A" && \
    echo "a" > a.txt && \
    jj new -m "Add file B" && \
    echo "b" > b.txt && \
    jj new -m "Add file C" && \
    echo "c" > c.txt

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/repo - jj repository with 3 commits: "Add file A", "Add file B", "Add file C"
#   - The working copy is at "Add file C" with c.txt

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]

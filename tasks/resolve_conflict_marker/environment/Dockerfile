FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Jujutsu (jj) project with a conflicted file file.txt in /home/user/myproject."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    jj git init --colocate && \
    echo "base" > file.txt && \
    jj commit -m "base" && \
    echo "A" > file.txt && \
    jj commit -m "A" && \
    jj new @-- && \
    echo "B" > file.txt && \
    jj commit -m "B" && \
    jj rebase -r @ -d @--+

# Container contents:
#   - jj installed in /usr/local/bin.
#   - /home/user/myproject  — jj project repository.
#   - file.txt containing conflict markers resulting from a rebase.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]

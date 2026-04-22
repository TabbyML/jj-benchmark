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
LABEL Description="jj task environment with a pre-existing commit stack (A -> B -> C) in /home/user/myproject."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    jj config set --user user.name "Your Name" && \
    jj config set --user user.email "your@email.com" && \
    jj git init --colocate && \
    echo "A" > file_a.txt && \
    jj describe -m "commit A" && \
    jj new -m "commit B" && \
    echo "B" > file_b.txt && \
    jj new -m "commit C" && \
    echo "C" > file_c.txt

# Container contents:
#   - jj v0.38.0 installed
#   - /home/user/myproject — initialized jj repository with a commit stack: A -> B -> C

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
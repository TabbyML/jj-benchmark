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
LABEL Description="jj project with unresolved conflicts in file1.txt and file2.txt."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    jj git init && \
    jj config set --user user.name "Your Name" && \
    jj config set --user user.email "your@email.com" && \
    echo "base 1" > file1.txt && \
    echo "base 2" > file2.txt && \
    jj commit -m "base" && \
    jj bookmark create base && \
    jj new -m "side 1" && \
    echo "side 1" > file1.txt && \
    echo "side 1" > file2.txt && \
    jj commit -m "side 1" && \
    jj bookmark create side1 && \
    jj new base -m "side 2" && \
    echo "side 2" > file1.txt && \
    echo "side 2" > file2.txt && \
    jj commit -m "side 2" && \
    jj bookmark create side2 && \
    jj new side1 side2 -m "merge"

# Container contents:
#   - jj installed in /usr/local/bin/jj
#   - /home/user/myproject - jj project with unresolved conflicts in file1.txt and file2.txt

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
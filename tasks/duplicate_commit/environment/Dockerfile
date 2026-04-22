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
LABEL Description="Jujutsu repository with two branches to test jj duplicate."

RUN git config --global user.name "Test User" && \
    git config --global user.email "test@example.com" && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

RUN mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj git init && \
    jj new 'root()' -m "Initial commit" && \
    echo "base" > base.txt && \
    jj bookmark create base && \
    jj new base -m "Feature A changes" && \
    echo "A" > a.txt && \
    jj bookmark create feature-a && \
    jj new base -m "Feature B changes" && \
    echo "B" > b.txt && \
    jj bookmark create feature-b && \
    jj new base -m "Work in progress"

# Container contents:
#   - jj installed
#   - /home/user/repo initialized as a jj repository
#   - Bookmarks 'feature-a' and 'feature-b' created

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
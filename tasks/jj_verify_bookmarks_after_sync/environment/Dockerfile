FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "aarch64" ]; then \
        curl -L -o jj.tar.gz https://github.com/martinvonz/jj/releases/download/v0.26.0/jj-v0.26.0-aarch64-unknown-linux-musl.tar.gz; \
    else \
        curl -L -o jj.tar.gz https://github.com/martinvonz/jj/releases/download/v0.26.0/jj-v0.26.0-x86_64-unknown-linux-musl.tar.gz; \
    fi && \
    tar -xzf jj.tar.gz && \
    find . -name jj -type f -exec mv {} /usr/local/bin/ \; && \
    rm -rf jj.tar.gz jj-v0.26.0-*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo with diverged feature-x bookmark"

RUN mkdir -p /home/user/remote_repo && \
    cd /home/user/remote_repo && \
    git init --bare && \
    cd /home/user && \
    git clone /home/user/remote_repo temp_clone && \
    cd temp_clone && \
    git config user.name "Teammate" && \
    git config user.email "teammate@example.com" && \
    echo "Initial commit" > README.md && \
    git add README.md && \
    git commit -m "Initial commit" && \
    git push origin master && \
    git checkout -b feature-x && \
    echo "Feature X base" > feature.txt && \
    git add feature.txt && \
    git commit -m "Feature X base" && \
    git push origin feature-x && \
    cd /home/user && \
    jj git clone /home/user/remote_repo repo && \
    cd repo && \
    jj config set --repo user.name "User" && \
    jj config set --repo user.email "user@example.com" && \
    jj bookmark track feature-x@origin && \
    jj new feature-x -m "Local change to feature X" && \
    echo "Local change" >> feature.txt && \
    jj bookmark move feature-x --to @ && \
    cd /home/user/temp_clone && \
    echo "Remote change" >> feature.txt && \
    git add feature.txt && \
    git commit -m "Remote change to feature X" && \
    git push origin feature-x && \
    cd /home/user && \
    rm -rf temp_clone

CMD ["/bin/bash"]

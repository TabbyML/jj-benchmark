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
LABEL Description="jj repo with a bookmark conflict scenario on feature-login."

RUN git init --bare /home/user/remote.git && \
    jj git clone /home/user/remote.git /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com" && \
    jj new 'root()' -m "Initial commit" && \
    echo "initial" > file.txt && \
    jj bookmark create main -r @ && \
    jj git push --all && \
    jj new main -m "Base feature commit" && \
    echo "base" > feature.txt && \
    jj bookmark create feature-login -r @ && \
    jj git push --allow-new --bookmark feature-login && \
    jj git clone /home/user/remote.git /home/user/temp_repo && \
    cd /home/user/temp_repo && \
    jj config set --repo user.name "Coworker" && \
    jj config set --repo user.email "coworker@example.com" && \
    jj bookmark track feature-login@origin && \
    jj new feature-login -m "Coworker commit" && \
    echo "coworker" >> feature.txt && \
    jj bookmark set feature-login -r @ && \
    jj git push --bookmark feature-login && \
    cd /home/user/repo && \
    jj new feature-login -m "My local commit" && \
    echo "my local" >> feature.txt && \
    jj bookmark set feature-login -r @

# Container contents:
#   - /home/user/remote.git - bare git repository serving as the origin
#   - /home/user/repo - local jj repository with 'feature-login' bookmark diverged from the remote
#   - /home/user/temp_repo - temporary clone used to create the remote divergence
#   - Python 3, pip, and pytest available for automated verification.

CMD ["/bin/bash"]

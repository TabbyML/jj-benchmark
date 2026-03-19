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
LABEL Description="Git repository at /home/user/my-project with one initial commit, ready for jj colocation."

RUN git config --global user.name "Test User" && \
    git config --global user.email "test@example.com" && \
    mkdir -p /home/user/my-project && \
    cd /home/user/my-project && \
    git init --initial-branch=main && \
    echo "initial commit" > README.md && \
    git add README.md && \
    git commit -m "Initial commit"

# Container contents:
#   - /home/user/my-project - A standard Git repository with one initial commit on main branch.
#   - jj binary installed in /usr/local/bin
#   - Python 3 and pytest available for automated verification.

CMD ["/bin/bash"]

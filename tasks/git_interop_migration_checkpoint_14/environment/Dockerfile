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
LABEL Description="Git repository in /home/user/project with a main branch and app.py."

RUN mkdir -p /home/user/project && \
    cd /home/user/project && \
    git init && \
    git config user.name "Test User" && \
    git config user.email "test@example.com" && \
    echo "def main():" > app.py && \
    echo "    pass" >> app.py && \
    git add app.py && \
    git commit -m "Initial commit" && \
    git branch -m main

# Container contents:
#   - /home/user/project - A local Git repository with an initial commit on the 'main' branch containing app.py.

CMD ["/bin/bash"]

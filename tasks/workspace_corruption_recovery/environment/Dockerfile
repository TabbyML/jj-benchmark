FROM ubuntu:24.04

RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl ca-certificates git python3 python3-pip python3-pytest bash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN jj config set --user user.name "Test User" && jj config set --user user.email "test@example.com"

# Initialize the main repo
RUN cd /home/user && jj git init repo

# Create some initial commits in main repo
RUN cd /home/user/repo && \
    echo "project init" > README.md && \
    jj describe -m "Initial project setup" && \
    jj new -m "Add core module" && \
    echo "def core(): pass" > core.py && \
    jj bookmark create main -r @

# Create a secondary workspace
RUN cd /home/user/repo && \
    jj workspace add /home/user/secondary-ws --name secondary

# Do some work in the secondary workspace
RUN cd /home/user/secondary-ws && \
    jj describe -m "WIP: secondary workspace changes" && \
    echo "secondary work" > secondary_feature.py

# Record the secondary workspace's working copy commit ID
RUN cd /home/user/secondary-ws && \
    jj log --no-graph -T 'change_id.short() ++ "\n"' -r '@' > /home/user/secondary_wc_id.txt && \
    cat /home/user/secondary_wc_id.txt

# From the main workspace, abandon the secondary workspace's working copy commit
# This creates the stale workspace condition
RUN cd /home/user/repo && \
    SEC_ID=$(cat /home/user/secondary_wc_id.txt) && \
    jj abandon "$SEC_ID"

# Create a workspace status report showing the stale condition
RUN cd /home/user/repo && \
    jj workspace list > /home/user/workspace_status_before.txt 2>&1 || true && \
    cat /home/user/workspace_status_before.txt

CMD ["/bin/bash"]

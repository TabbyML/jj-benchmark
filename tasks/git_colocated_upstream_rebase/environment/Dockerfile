FROM ubuntu:24.04

RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    curl ca-certificates git python3 python3-pip python3-pytest bash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

# Configure git globally too
RUN git config --global user.name "Test User" && \
    git config --global user.email "test@example.com" && \
    git config --global init.defaultBranch main

# Create the "upstream" bare git repo (simulates a remote server)
RUN mkdir -p /home/user/upstream.git && \
    cd /home/user/upstream.git && \
    git init --bare

# Create an intermediate git repo to populate the upstream
RUN mkdir -p /home/user/upstream-local && \
    cd /home/user/upstream-local && \
    git init && \
    echo "# Upstream Project" > README.md && \
    echo "version=1.0" > version.txt && \
    git add -A && git commit -m "upstream-1: initial project" && \
    echo "feature=auth" > features.txt && \
    git add -A && git commit -m "upstream-2: add features list" && \
    git remote add origin /home/user/upstream.git && \
    git push origin main

# Clone from upstream into the local jj-colocated repo
RUN cd /home/user && \
    jj git clone /home/user/upstream.git local-repo --colocate

# Add 2 more commits to upstream that the local repo doesn't have yet
RUN cd /home/user/upstream-local && \
    echo "security=strict" >> features.txt && \
    echo "max_connections=100" >> version.txt && \
    git add -A && git commit -m "upstream-3: add security config" && \
    echo "cache_ttl=3600" >> version.txt && \
    echo "log_level=INFO" >> features.txt && \
    git add -A && git commit -m "upstream-4: add cache and logging config" && \
    git push origin main

# Now create 3 local commits on top of the OLD upstream head (before upstream advanced)
RUN cd /home/user/local-repo && \
    jj new -m "local-1: add user service" && \
    echo "def get_user(): pass" > user_service.py

RUN cd /home/user/local-repo && \
    jj new -m "local-2: add product service" && \
    echo "def get_product(): pass" > product_service.py

RUN cd /home/user/local-repo && \
    jj new -m "local-3: add order service" && \
    echo "def create_order(): pass" > order_service.py

RUN cd /home/user/local-repo && \
    jj bookmark create local-branch -r @

# Save the current state
RUN cd /home/user/local-repo && \
    jj log --no-graph -r 'all()' \
        -T 'change_id.short() ++ " " ++ description ++ "\n"' \
        > /home/user/local_state.txt

CMD ["/bin/bash"]

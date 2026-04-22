FROM pochi-browser-verification-base

# Install prerequisites
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install pip packages
RUN pip3 install --break-system-packages pytest

# Install jj
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

# Create /home/user as root
RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="jj environment with a cloned repo and unpushed changes."

# Setup the environment
RUN cd /home/user && \
    git config --global user.name "Test User" && \
    git config --global user.email "test@example.com" && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    git init --bare remote.git && \
    jj git clone remote.git repo && \
    cd repo && \
    echo "This is a new feature" > feature.txt

# Container contents:
#   - jj and git installed.
#   - /home/user/remote.git - bare git repository
#   - /home/user/repo - jj repository cloned from remote.git with a new file feature.txt

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]

FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip bash && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install jj v0.38.0
RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

# Create home directory
RUN mkdir -p /home/user && chmod 0755 /home/user

# Configure jj user identity (required for jj commands to work)
RUN mkdir -p /home/user/.config/jj && \
    printf '[user]\nname = "Dev User"\nemail = "dev@example.com"\n' \
        > /home/user/.config/jj/config.toml

# Initialise the jj git-backed repository
RUN jj git init /home/user/myrepo

# Create src/main.py (should remain tracked)
RUN mkdir -p /home/user/myrepo/src && \
    printf 'def main():\n    print("Hello, world!")\n\nif __name__ == "__main__":\n    main()\n' \
        > /home/user/myrepo/src/main.py

# Create build/output.bin (build artifact — should be untracked by user)
RUN mkdir -p /home/user/myrepo/build && \
    echo "binary-output-data" > /home/user/myrepo/build/output.bin

# Snapshot both files into the working-copy commit by running jj status
RUN jj -R /home/user/myrepo --config "user.name=Dev User" --config "user.email=dev@example.com" status

# Describe the working-copy commit
RUN jj -R /home/user/myrepo --config "user.name=Dev User" --config "user.email=dev@example.com" \
    describe -m "initial files with build artifact"

LABEL Author="jj-task-builder"
LABEL Description="jj repo with src/main.py and build/output.bin tracked; user must add .gitignore and untrack build artifact."

# Working state:
# - /home/user/myrepo is a valid jj git-backed repo
# - /home/user/myrepo/src/main.py is tracked in working-copy commit
# - /home/user/myrepo/build/output.bin is tracked in working-copy commit
# - No .gitignore exists yet
# Task: add build/ to .gitignore, then run jj file untrack build/output.bin

CMD ["/bin/bash"]

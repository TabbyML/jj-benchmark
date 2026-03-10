FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/martinvonz/jj/releases/download/v0.26.0/jj-v0.26.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="jj-task-builder"
LABEL Description="jj repo with main and feature branches, ready for duplicate and rebase task."

RUN jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com" && \
    jj config set --user ui.color "never" && \
    mkdir -p /home/user/repo && \
    cd /home/user/repo && \
    jj git init && \
    cat > app.py << 'EOF'
def main():
    print("Hello from main")
EOF
RUN cd /home/user/repo && \
    jj new -m "Initial commit on main" && \
    jj bookmark create main && \
    jj new main -m "Add hello_world function" && \
    cat > app.py << 'EOF'
def main():
    print("Hello from main")

def hello_world():
    print("Hello world!")
EOF
RUN cd /home/user/repo && \
    jj bookmark create feature && \
    jj new main -m "Update main" && \
    cat > utils.py << 'EOF'
def helper():
    pass
EOF
RUN cd /home/user/repo && \
    jj bookmark move main && \
    jj new main

CMD ["/bin/bash"]

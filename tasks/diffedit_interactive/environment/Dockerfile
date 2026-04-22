FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL \
    https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="jj project with an initial commit containing foo() and bar()."

RUN mkdir -p /home/user/myproject && \
    cd /home/user/myproject && \
    jj config set --user user.name "Your Name" && \
    jj config set --user user.email "your@email.com" && \
    jj git init --colocate && \
    cat >app.py <<'EOF'
def foo():
    print("foo")

def bar():
    print("bar")
EOF
RUN cd /home/user/myproject && jj commit -m "add features"

# Container contents:
#   - jj installed
#   - /home/user/myproject: jj project with a commit "add features" containing foo() and bar()

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]

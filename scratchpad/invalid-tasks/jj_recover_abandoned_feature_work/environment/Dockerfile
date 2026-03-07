FROM ubuntu:22.04

LABEL Author="jj-task-builder"
LABEL Description="jj task: recover abandoned feature work using op log and op restore"

ENV DEBIAN_FRONTEND=noninteractive
ENV EDITOR=true

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    git \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pytest

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN mkdir -p /home/user/project

RUN jj git init /home/user/project

RUN jj -R /home/user/project config set --repo user.name "Support Engineer"
RUN jj -R /home/user/project config set --repo user.email "support@example.com"

RUN echo "# Project" > /home/user/project/README.md && \
    jj -R /home/user/project describe -m "initial project setup"

RUN jj -R /home/user/project bookmark create main -r @

RUN jj -R /home/user/project new -m "add login page skeleton"

RUN cat > /home/user/project/login.py << 'EOF'
# Login page skeleton
def login(username, password):
    """Authenticate a user."""
    # TODO: implement authentication logic
    pass

def logout():
    """Log out the current user."""
    pass
EOF

RUN jj -R /home/user/project new

RUN jj -R /home/user/project abandon @-

CMD ["/bin/bash"]

FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

RUN git config --global user.name "Contributor" && \
    git config --global user.email "contributor@example.com"

RUN jj config set --user user.name "Contributor" && \
    jj config set --user user.email "contributor@example.com"

# Initialize shared repo
RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Contributor" && \
    jj config set --repo user.email "contributor@example.com"

# Base commit with src/api.py
RUN mkdir -p /home/user/repo/src && \
    printf 'from flask import Flask\napp = Flask(__name__)\n\n@app.route("/")\ndef index():\n    return "hello"\n' > /home/user/repo/src/api.py && \
    cd /home/user/repo && \
    jj describe -m "init: base api" && \
    jj bookmark create main -r @

# Create ws-a workspace: add new endpoint /users
RUN jj --repository /home/user/repo workspace add /home/user/ws-a --name ws-a
RUN cd /home/user/ws-a && \
    jj new main && \
    printf 'from flask import Flask\napp = Flask(__name__)\n\n@app.route("/")\ndef index():\n    return "hello"\n\n@app.route("/users")\ndef get_users():\n    return {"users": []}\n' > src/api.py && \
    jj describe -m "feat: add users endpoint" && \
    jj bookmark create feature-a -r @

# Create ws-b workspace: add different endpoint /products from main (diverging)
RUN jj --repository /home/user/repo workspace add /home/user/ws-b --name ws-b
RUN cd /home/user/ws-b && \
    jj new main && \
    printf 'from flask import Flask\napp = Flask(__name__)\n\n@app.route("/")\ndef index():\n    return "hello world"\n\n@app.route("/products")\ndef get_products():\n    return {"products": []}\n' > src/api.py && \
    jj describe -m "feat: add products endpoint" && \
    jj bookmark create feature-b -r @

LABEL Description="Two jj workspaces (ws-a, ws-b) both modified src/api.py from main. ws-b needs rebase onto ws-a, conflict resolution, then merge into main."

CMD ["/bin/bash"]

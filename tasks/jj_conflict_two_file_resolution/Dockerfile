FROM jj-task-base:latest

LABEL Author="jj-task-builder"
LABEL Description="jj repo with conflicts in two config files after rebase"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf 'host=localhost\n' > server.cfg && \
    printf 'port=8080\n' > client.cfg && \
    jj describe -m "base: add configs" && \
    jj bookmark create base -r @ && \
    jj new

RUN cd /home/user/repo && \
    printf 'host=prod.server.com\n' > server.cfg && \
    printf 'port=443\n' > client.cfg && \
    jj describe -m "main: update configs" && \
    jj bookmark create main -r @ && \
    jj new base

RUN cd /home/user/repo && \
    printf 'host=dev.server.com\n' > server.cfg && \
    printf 'port=9090\n' > client.cfg && \
    jj describe -m "feat: feature configs" && \
    jj bookmark create feature -r @ && \
    jj new

RUN cd /home/user/repo && \
    jj rebase -b feature --onto main

CMD ["/bin/bash"]

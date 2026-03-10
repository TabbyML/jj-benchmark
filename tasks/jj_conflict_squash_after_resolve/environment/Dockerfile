FROM jj-task-base:latest

LABEL Author="jj-task-builder"
LABEL Description="jj repo with conflict in data.json, resolve then squash into parent"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf '{"value": 0}\n' > data.json && \
    jj describe -m "base: init data" && \
    jj bookmark create base -r @ && \
    jj new

RUN cd /home/user/repo && \
    printf '{"value": 10}\n' > data.json && \
    jj describe -m "main: set value 10" && \
    jj bookmark create main -r @ && \
    jj new base

RUN cd /home/user/repo && \
    printf '{"value": 20}\n' > data.json && \
    jj describe -m "feat: set value 20" && \
    jj bookmark create feature -r @ && \
    jj new

RUN cd /home/user/repo && \
    jj rebase -b feature --onto main

CMD ["/bin/bash"]

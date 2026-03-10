FROM jj-task-base:latest

LABEL Author="jj-task-builder"
LABEL Description="jj repo with conflict in service.yaml for status reporting exercise"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf 'replicas: 1\n' > service.yaml && \
    jj describe -m "base: add service config" && \
    jj bookmark create base -r @ && \
    jj new

RUN cd /home/user/repo && \
    printf 'replicas: 3\n' > service.yaml && \
    jj describe -m "main: scale to 3" && \
    jj bookmark create main -r @ && \
    jj new base

RUN cd /home/user/repo && \
    printf 'replicas: 5\n' > service.yaml && \
    jj describe -m "feat: scale to 5" && \
    jj bookmark create feature -r @ && \
    jj new

RUN cd /home/user/repo && \
    jj rebase -b feature --onto main

CMD ["/bin/bash"]

FROM jj-task-base:latest

LABEL Author="jj-task-builder"
LABEL Description="jj repo with conflict in config.py for undo-and-reresolve exercise"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf 'TIMEOUT = 10\n' > config.py && \
    jj describe -m "base: add config" && \
    jj bookmark create base -r @ && \
    jj new

RUN cd /home/user/repo && \
    printf 'TIMEOUT = 60\n' > config.py && \
    jj describe -m "main: increase timeout" && \
    jj bookmark create main -r @ && \
    jj new base

RUN cd /home/user/repo && \
    printf 'TIMEOUT = 30\n' > config.py && \
    jj describe -m "feat: custom timeout" && \
    jj bookmark create feature -r @ && \
    jj new

RUN cd /home/user/repo && \
    jj rebase -b feature --onto main

CMD ["/bin/bash"]

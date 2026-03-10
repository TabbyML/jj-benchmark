FROM jj-task-base:latest

LABEL Author="jj-task-builder"
LABEL Description="jj repo with conflict in config.txt after feature rebased onto main"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf 'setting=on\n' > config.txt && \
    jj describe -m "base: add config" && \
    jj bookmark create base -r @ && \
    jj new

RUN cd /home/user/repo && \
    printf 'setting=main\n' > config.txt && \
    jj describe -m "main: main change" && \
    jj bookmark create main -r @ && \
    jj new base

RUN cd /home/user/repo && \
    printf 'setting=feature\n' > config.txt && \
    jj describe -m "feat: feature change" && \
    jj bookmark create feature -r @ && \
    jj new

RUN cd /home/user/repo && \
    jj rebase -b feature --onto main

CMD ["/bin/bash"]

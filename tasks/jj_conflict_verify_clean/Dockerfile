FROM jj-task-base:latest

LABEL Author="jj-task-builder"
LABEL Description="jj repo with conflict in settings.ini for verification workflow exercise"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf 'mode=default\n' > settings.ini && \
    jj describe -m "base: add settings" && \
    jj bookmark create base -r @ && \
    jj new

RUN cd /home/user/repo && \
    printf 'mode=production\n' > settings.ini && \
    jj describe -m "main: set production mode" && \
    jj bookmark create main -r @ && \
    jj new base

RUN cd /home/user/repo && \
    printf 'mode=debug\n' > settings.ini && \
    jj describe -m "feat: set debug mode" && \
    jj bookmark create feature -r @ && \
    jj new

RUN cd /home/user/repo && \
    jj rebase -b feature --onto main

CMD ["/bin/bash"]

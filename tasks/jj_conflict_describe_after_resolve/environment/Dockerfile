FROM jj-task-base:latest

LABEL Author="jj-task-builder"
LABEL Description="jj repo with conflict in README.md, focus on describe after resolve"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf '# Project\nVersion: 1\n' > README.md && \
    jj describe -m "docs: add readme" && \
    jj bookmark create base -r @ && \
    jj new

RUN cd /home/user/repo && \
    printf '# Project\nVersion: 2\n' > README.md && \
    jj describe -m "docs: update to v2" && \
    jj bookmark create main -r @ && \
    jj new base

RUN cd /home/user/repo && \
    printf '# Project\nVersion: 3\n' > README.md && \
    jj describe -m "docs: update to v3" && \
    jj bookmark create feature -r @ && \
    jj new

RUN cd /home/user/repo && \
    jj rebase -b feature --onto main

CMD ["/bin/bash"]

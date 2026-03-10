FROM jj-task-base:latest

LABEL Author="jj-task-builder"
LABEL Description="jj repo with conflicts in three files (api.py, db.py, ui.py) for multi-file report exercise"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf 'API_VERSION=1\n' > api.py && \
    printf 'DB_VERSION=1\n' > db.py && \
    printf 'UI_VERSION=1\n' > ui.py && \
    jj describe -m "base: add project files" && \
    jj bookmark create base -r @ && \
    jj new

RUN cd /home/user/repo && \
    printf 'API_VERSION=2\n' > api.py && \
    printf 'DB_VERSION=2\n' > db.py && \
    printf 'UI_VERSION=2\n' > ui.py && \
    jj describe -m "main: bump all versions" && \
    jj bookmark create main -r @ && \
    jj new base

RUN cd /home/user/repo && \
    printf 'API_VERSION=3\n' > api.py && \
    printf 'DB_VERSION=3\n' > db.py && \
    printf 'UI_VERSION=3\n' > ui.py && \
    jj describe -m "feat: feature versions" && \
    jj bookmark create feature -r @ && \
    jj new

RUN cd /home/user/repo && \
    jj rebase -b feature --onto main

CMD ["/bin/bash"]

FROM jj-task-base:latest

LABEL Author="jj-task-builder"
LABEL Description="jj repo with chained commits rebased onto main, conflict in first chain commit"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf 'X=1\n' > vars.sh && \
    jj describe -m "base: init" && \
    jj bookmark create base -r @ && \
    jj new

RUN cd /home/user/repo && \
    printf 'X=10\n' > vars.sh && \
    jj describe -m "main: set X=10" && \
    jj bookmark create main -r @ && \
    jj new base

RUN cd /home/user/repo && \
    printf 'X=2\n' > vars.sh && \
    jj describe -m "chain: set X=2" && \
    jj bookmark create chain_a -r @

RUN cd /home/user/repo && \
    jj new chain_a && \
    printf 'X=2\nY=X\n' > vars.sh && \
    jj describe -m "chain: set Y=X" && \
    jj bookmark create chain_b -r @ && \
    jj new

RUN cd /home/user/repo && \
    jj rebase -b chain_b --onto main

CMD ["/bin/bash"]

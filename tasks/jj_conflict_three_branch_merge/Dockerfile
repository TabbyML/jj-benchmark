FROM jj-task-base:latest

LABEL Author="jj-task-builder"
LABEL Description="jj repo with three branches modifying main.py, feat_b rebased onto feat_a"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf "MODE = 'base'\n" > main.py && \
    jj describe -m "base: init main" && \
    jj bookmark create base -r @ && \
    jj new

RUN cd /home/user/repo && \
    printf "MODE = 'A'\n" > main.py && \
    jj describe -m "feat: mode A" && \
    jj bookmark create feat_a -r @ && \
    jj new base

RUN cd /home/user/repo && \
    printf "MODE = 'B'\n" > main.py && \
    jj describe -m "feat: mode B" && \
    jj bookmark create feat_b -r @ && \
    jj new

RUN cd /home/user/repo && \
    jj rebase -b feat_b --onto feat_a

CMD ["/bin/bash"]

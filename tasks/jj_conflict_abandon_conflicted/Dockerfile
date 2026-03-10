FROM jj-task-base:latest

LABEL Author="jj-task-builder"
LABEL Description="jj repo with conflicted feature commit to be abandoned and recreated cleanly"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf '#!/bin/bash\nBUILD=1\n' > build.sh && \
    jj describe -m "base: init" && \
    jj bookmark create base -r @ && \
    jj new

RUN cd /home/user/repo && \
    printf '#!/bin/bash\nBUILD=10\nOPT=fast\n' > build.sh && \
    jj describe -m "main: update build" && \
    jj bookmark create main -r @ && \
    jj new base

RUN cd /home/user/repo && \
    printf '#!/bin/bash\nBUILD=99\nCUSTOM=true\n' > build.sh && \
    jj describe -m "feat: custom build" && \
    jj bookmark create feature -r @ && \
    jj new

RUN cd /home/user/repo && \
    jj rebase -b feature --onto main

CMD ["/bin/bash"]

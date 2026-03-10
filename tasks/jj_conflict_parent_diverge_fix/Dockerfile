FROM jj-task-base:latest

LABEL Author="jj-task-builder"
LABEL Description="jj repo with diverged branches both modifying params.env, branch_b rebased onto branch_a"

RUN jj git init /home/user/repo && \
    cd /home/user/repo && \
    jj config set --repo user.name "Test User" && \
    jj config set --repo user.email "test@example.com"

RUN cd /home/user/repo && \
    printf 'DB_HOST=localhost\nDB_PORT=5432\n' > params.env && \
    jj describe -m "base: set params" && \
    jj bookmark create base -r @ && \
    jj new

RUN cd /home/user/repo && \
    printf 'DB_HOST=db.prod.internal\nDB_PORT=5432\n' > params.env && \
    jj describe -m "ops: update DB host" && \
    jj bookmark create branch_a -r @ && \
    jj new base

RUN cd /home/user/repo && \
    printf 'DB_HOST=localhost\nDB_PORT=5433\n' > params.env && \
    jj describe -m "ops: update DB port" && \
    jj bookmark create branch_b -r @ && \
    jj new

RUN cd /home/user/repo && \
    jj rebase -b branch_b --onto branch_a

CMD ["/bin/bash"]

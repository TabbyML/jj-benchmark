FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz \
    | tar -xz -C /usr/local/bin ./jj

RUN mkdir -p /home/user && chmod 0755 /home/user

WORKDIR /home/user

RUN git config --global user.name "Test User" && \
    git config --global user.email "test@example.com" && \
    jj config set --user user.name "Test User" && \
    jj config set --user user.email "test@example.com"

RUN mkdir -p upstream.git && \
    cd upstream.git && \
    git init --bare --initial-branch=main && \
    cd .. && \
    mkdir -p project && \
    cd project && \
    git init --initial-branch=main && \
    echo "console.log('init');" > main.js && \
    git add main.js && \
    git commit -m "initial commit" && \
    git remote add origin ../upstream.git && \
    git push -u origin main && \
    cd ../upstream.git && \
    cd ../project && \
    echo "console.log('upstream change');" >> main.js && \
    git commit -am "upstream commit" && \
    git push origin main && \
    git reset --hard HEAD~1 && \
    git remote remove origin && \
    echo "console.log('local change');" >> main.js && \
    git commit -am "local commit"

CMD ["/bin/bash"]

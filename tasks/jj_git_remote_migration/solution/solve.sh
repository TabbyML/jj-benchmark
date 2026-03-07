#!/bin/bash
set -euo pipefail

cd /home/user/project
jj git init --colocate
jj git remote add upstream /home/user/upstream.git
jj git fetch --remote upstream
jj rebase -r @ -d main@upstream

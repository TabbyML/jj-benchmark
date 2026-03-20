#!/usr/bin/env bash

cd /home/user/repo

# 1. Find the abandoned revision
# It was deleted recently, so it's in the op log. We can use the description to find it.
# jj log --at-op @- -r 'description("*feature-x work*")'
# Wait, actually to restore it, we can just find its change ID from the op log or from `jj log -r 'description("*feature-x work*")' --at-op @-`
REV=$(jj log --at-op @- -r 'description("*feature-x work*")' --no-graph -T 'commit_id')

# 2. Restore the bookmark `feature-x`
jj bookmark create feature-x -r $REV

# 3. Rebase `feature-x` onto the `main` branch
jj rebase -b feature-x -d main

# 4. Save the output of `jj log -r feature-x` to `/home/user/log.txt`
jj log -r feature-x > /home/user/log.txt

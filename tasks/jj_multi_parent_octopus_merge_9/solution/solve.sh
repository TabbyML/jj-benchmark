#!/bin/bash
cd /home/user/octopus_repo
BASE_REV=$(jj log -r @ --no-graph -T 'commit_id')

# branch a
jj new $BASE_REV -m "branch a"
echo "a" > a.txt
jj bookmark create branch_a -r @

# branch b
jj new $BASE_REV -m "branch b"
echo "b" > b.txt
jj bookmark create branch_b -r @

# branch c
jj new $BASE_REV -m "branch c"
echo "c" > c.txt
jj bookmark create branch_c -r @

# octopus merge
jj new branch_a branch_b branch_c -m "octopus merge"
jj bookmark create octopus_merge -r @

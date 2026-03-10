#!/bin/bash
set -euo pipefail

cd /home/user/repo

# 1. Duplicate the commit pointed to by the `feature` bookmark.
# 2. Rebase the duplicated commit so that it is a child of the `main` bookmark.
jj duplicate feature --destination main

# 3. Create a new bookmark called `feature-experiment` pointing to this newly duplicated and rebased commit.
# The new commit is a head of main, but not the working copy (@)
jj bookmark create feature-experiment -r 'heads(main::) ~ @'


#!/bin/bash
set -e

cd /home/user/myrepo

# Find the abandoned commit ID from the op log
COMMIT_ID=$(jj op log --no-pager | grep "abandon commit" | head -n 1 | awk '{print $4}')

# Create the recovered-login bookmark pointing to the abandoned commit
jj bookmark create recovered-login -r $COMMIT_ID

#!/bin/bash

cd /home/user/repo

# Move feature-x bookmark to working copy
jj bookmark move feature-x -to @

# Create bugfix-y bookmark on parent of working copy
jj bookmark create bugfix-y -r @-

# Verify and save
jj log -r 'bugfix-y..feature-x' -T 'bookmarks ++ "\n"' > /home/user/bookmark_verification.log

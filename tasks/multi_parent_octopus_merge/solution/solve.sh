#!/bin/bash
cd /home/user/project
jj new feature-a feature-b feature-c -m "Merge three features"
echo "merged" > octopus.txt
jj bookmark create integration -r @
jj log -r 'parents(integration)' -T 'bookmarks ++ "\n"' > /home/user/parents.log
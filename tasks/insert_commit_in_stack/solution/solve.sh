#!/bin/bash
set -e
cd /home/user/repo
# Use the commit with description starting with B
jj new -B "description(exact:\"B\n\")" -m "Add config"
echo "base=true" > config.txt
jj new "description(exact:\"C\n\")"

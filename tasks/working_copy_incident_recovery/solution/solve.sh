#!/bin/bash
cd /home/user/repo
jj restore data/cache.bin
jj restore scripts/deploy.sh
jj commit -m "chore: update settings for incident recovery"
jj log --no-graph -r @ -T commit_id > /home/user/recovery_status.txt

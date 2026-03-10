#!/bin/bash

cd /home/user/project-alpha

cat << 'EOF' > config.yaml
version: 1.0
environment: production
feature_flag: enabled
EOF

jj resolve --mark config.yaml

jj log -r @ > /home/user/jj_conflict_resolution_log.txt

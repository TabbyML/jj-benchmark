#!/bin/bash
set -e

cd /home/user/repo

# Find the two divergent commits. We can identify them by the change ID or bookmark.
# Since we fetched, they are marked as feature@git and feature@origin (if tracking).
# However, to be robust, we can just find the two commits with the same change ID.
# But jj squash --from feature@git --into feature@origin works.
# Let's use that.
jj squash --from feature@git --into feature@origin -m "resolved divergence"

# Get the change ID of the squashed commit. It's the one with description "resolved divergence"
# Wait, jj squash might have kept the change ID of feature@origin.
SQUASHED_REV=$(jj log --no-graph -r 'description("resolved divergence")' -T commit_id)

# Set the bookmark to the new commit to resolve bookmark conflict
jj bookmark set feature -r "$SQUASHED_REV"

# Create a new commit to resolve the file conflict
jj new "$SQUASHED_REV"

cat << 'EOF' > main.py
def main():
    print('local feature')
    print('remote bugfix')
EOF

# Squash the resolution into the feature commit
jj squash

# Write the change ID
jj log -r feature --no-graph -T change_id > /home/user/resolved_change_id.txt

# Write the main.py content
cat main.py > /home/user/main_content.txt

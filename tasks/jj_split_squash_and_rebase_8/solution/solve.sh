#!/bin/bash
cd /home/user/repo

# Get the commit ID of the second commit ("mixed changes")
MIXED_COMMIT=$(jj log -r 'description("mixed changes")' --no-graph -T 'commit_id')

# Split the second commit
# We want utils.py in one commit and api.py in the other.
# We can do this with jj split, but it's interactive.
# Instead, we can use `jj restore` or `jj squash` to do it non-interactively.
# Let's create a new commit after "add utils.py"
ADD_UTILS=$(jj log -r 'description("add utils.py")' --no-graph -T 'commit_id')

# Move the api.py change out of the mixed commit
# Create a new commit for api.py
jj new $ADD_UTILS -m "api.py additions"
API_COMMIT=$(jj log -r @ --no-graph -T 'commit_id')
jj restore -c $MIXED_COMMIT --to @ api.py

# Now squash the remaining changes in MIXED_COMMIT (which is just utils.py) into ADD_UTILS
jj squash -r $MIXED_COMMIT --into $ADD_UTILS

# Rebase the remaining commits (the test commit and the new api commit)
# Wait, the test commit was a child of MIXED_COMMIT.
# Since we squashed MIXED_COMMIT into ADD_UTILS, the test commit is now a child of ADD_UTILS.
# Let's rebase the test commit onto the API_COMMIT.
TEST_COMMIT=$(jj log -r 'description("add tests")' --no-graph -T 'commit_id')
jj rebase -r $TEST_COMMIT -d $API_COMMIT

# Move the feature bookmark
jj bookmark move feature --to $TEST_COMMIT

# Generate result.txt
jj log -r 'main..feature' -T 'description ++ "\n"' --no-graph > /home/user/result.txt

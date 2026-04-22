# Split a Commit in Jujutsu

## Background
You are working on a project using `jj` (Jujutsu). You have a single commit that introduces two features at once, but you realize they should be separated into two distinct commits for a cleaner history.

## Requirements
- The repository is located at `/home/user/myproject`.
- The parent of the current working copy (`@-`) contains two files: `feature_a.py` and `feature_b.py`, and has the description "Add feature A and feature B".
- You must split this commit into two separate commits.
- The first commit (older) must contain ONLY `feature_a.py` and have the description exactly "Add feature A".
- The second commit (newer, child of the first) must contain ONLY `feature_b.py` and have the description exactly "Add feature B".
- The current working copy (`@`) should remain empty and be a child of the "Add feature B" commit.

## Constraints
- Project path: `/home/user/myproject`
- Use only `jj` commands.
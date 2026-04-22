# Squash Commits in Jujutsu

## Background
You are working in a `jj` repository at `/home/user/myproject`. The repository contains a chain of commits modifying `app.py`.

## Requirements
1. Squash the commit with the description "add feature B" into its parent commit (which has the description "add feature A").
2. The resulting combined commit must have the description "add feature A and B".
3. The descendant commit "add feature C" must remain intact and be rebased automatically by `jj`.

## Implementation
- Use `jj squash` or `jj rebase` to combine the commits.
- Update the description of the combined commit to "add feature A and B".
- All operations should be performed within `/home/user/myproject`.

## Constraints
- Project path: `/home/user/myproject`
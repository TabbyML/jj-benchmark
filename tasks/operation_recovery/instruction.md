# Undo Operations in Jujutsu

## Background
Every repository operation (commit, rebase, push) is recorded in `jj` and can be reverted using `jj undo`.

## Requirements
- You have a repository in `/home/user/project` with several recent operations.
- The operation log has 5 distinct operations beyond the initial setup.
- Undo back to the state immediately after the operation that created `file2.txt`.

## Implementation
1. Go to `/home/user/project`.
2. Run `jj op log` to view the history of operations.
3. Identify the operation ID where `Commit 2` (which added `file2.txt`) was created.
4. Run `jj undo <operation_id>` or `jj op restore <operation_id>` to return the repo to that state.

## Constraints
- Project path: `/home/user/project`.
# Simulating and Resolving Concurrent Operations in Jujutsu

## Background
Jujutsu (`jj`) uses an operation log to enable lock-free concurrency. It is possible to simulate divergent operations by running commands at a specific past operation using the `--at-operation=<operation ID>` flag.

## Requirements
1. In the repository at `/home/user/repo`, there is a change that was originally created with the description `Feature X`.
2. The repository currently has its description updated to `Feature X - variant 1`.
3. You need to simulate a concurrent operation by describing the commit as `Feature X - variant 2` at the exact operation ID where the `Feature X` commit was originally created (before it was updated to `variant 1`).
4. Trigger the operation log merge to see the divergence.
5. Resolve the divergence by keeping only the `Feature X - variant 2` commit and abandoning the `Feature X - variant 1` commit.

## Implementation Guide
1. Go to `/home/user/repo`.
2. Use `jj op log` to find the operation ID where `jj new -m 'Feature X'` was run (the `new empty commit` operation).
3. Run `jj --at-operation=<op_id> describe <change_id> -m 'Feature X - variant 2'`, replacing `<op_id>` with the operation ID from step 2, and `<change_id>` with the Change ID of the `Feature X` commit.
4. Run `jj st` to trigger the merge of the divergent operations.
5. Use `jj log` to see the divergent changes (they will share the same Change ID and have `??` after it).
6. Abandon the commit with the description `Feature X - variant 1` using `jj abandon <commit_id>`.

## Constraints
- Project path: `/home/user/repo`
- The final state must have only one visible commit for the `Feature X` change, with the description `Feature X - variant 2`.
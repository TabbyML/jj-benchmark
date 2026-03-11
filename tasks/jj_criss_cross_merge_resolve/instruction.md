# Criss-Cross Merge Resolution

## Context

You are a reviewer working on a repository at `/home/user/repo`. The repository has a complex criss-cross merge history:

- `main-v1` is the original base commit
- `branch-a` started from `main-v1`, then at some point merged `branch-b` into itself
- `branch-b` started from `main-v1`, then at some point merged `branch-a` into itself

This creates a criss-cross pattern where both branches have each other in their history, making traditional merges ambiguous.

## Files Involved

- `src/core.py` — modified by both branches with conflicting changes
- `src/utils.py` — modified by both branches with conflicting changes
- `src/feature_a.py` — unique to branch-a
- `src/feature_b.py` — unique to branch-b

## Your Task

1. **Identify** the common ancestor of `branch-a` and `branch-b` (the `main-v1` commit). Use `jj log` to inspect the history.

2. **Create** a new working commit starting from `main-v1` using `jj new`.

3. **Cherry-pick** (using `jj restore --from` or `jj squash`) the unique changes from both branches in logical order:
   - First apply the unique file changes from `branch-a`
   - Then apply the unique file changes from `branch-b`

4. **Resolve conflicts** in `src/core.py` and `src/utils.py`:
   - In `src/core.py`: the final file must contain both the `initialize()` function from branch-a AND the `shutdown()` function from branch-b.
   - In `src/utils.py`: the final file must contain both the `format_output()` function from branch-a AND the `parse_input()` function from branch-b.

5. **Ensure** `src/feature_a.py` and `src/feature_b.py` are both present in the working copy.

6. **Create** an `integration` bookmark pointing to the current working copy commit:
   ```
   jj bookmark create integration -r @
   ```

7. **Write** `/home/user/criss_cross_log.txt` with exactly this format:
   ```
   branch_a_tip: <change_id_of_branch_a_tip>
   branch_b_tip: <change_id_of_branch_b_tip>
   integration_commit: <change_id_of_integration_commit>
   ```
   Use `jj log -r 'branch-a' --no-graph -T 'change_id'` to get the change IDs.

## Constraints

- Do NOT use `git` commands for history manipulation — use only `jj` commands
- The `integration` bookmark must point to a commit with no conflict markers
- Both `src/feature_a.py` and `src/feature_b.py` must exist in the working copy
- `src/core.py` must contain both `initialize()` and `shutdown()` functions
- `src/utils.py` must contain both `format_output()` and `parse_input()` functions
- The log file must use the exact key names shown above

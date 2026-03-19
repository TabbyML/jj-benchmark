You are a contributor managing two workspaces that independently modified the same file, creating a cross-workspace conflict.

## Environment

Three locations linked to the same jj repository at `/home/user/repo`:
- Main workspace: `/home/user/repo` — `main` bookmark at `init: base api`
- Workspace A: `/home/user/ws-a` — `feature-a` bookmark, added `/users` endpoint to `src/api.py`
- Workspace B: `/home/user/ws-b` — `feature-b` bookmark, added `/products` endpoint AND changed the index return value in `src/api.py`

Both workspaces branched from `main` and modified `src/api.py` differently. When rebasing `feature-b` onto `feature-a`, there will be a conflict.

## Your Task

### Step 1 — Assess the conflict situation

In each workspace, run `jj status` and `jj log` to understand the current state. Confirm that both `feature-a` and `feature-b` are children of `main`, and they diverge.

### Step 2 — Rebase feature-b onto feature-a

In workspace `/home/user/ws-b`:
- Rebase the `feat: add products endpoint` commit onto `feature-a` using:
  `jj rebase -r feature-b -d feature-a`
- This will create a conflict in `src/api.py`

### Step 3 — Resolve the conflict

After the rebase creates a conflict in `src/api.py`:
- The final `src/api.py` must contain BOTH the `/users` endpoint AND the `/products` endpoint
- The index route should return `"hello world"` (from feature-b)
- Remove all conflict markers
- The file must have no `<<<<<<<`, `=======`, or `>>>>>>>` markers

### Step 4 — Verify workspace B is clean

After resolving the conflict:
- Run `jj status` in `/home/user/ws-b` to confirm no conflicts remain
- Move `feature-b` bookmark to point to the rebased commit

### Step 5 — Merge both features into main

In the main workspace at `/home/user/repo`:
- Create a merge commit: `jj new feature-a feature-b`
- Verify no conflicts exist in the merge
- Move `main` bookmark to the merge commit: `jj bookmark set main -r @`

### Step 6 — Write the cross-boundary log

Write `/home/user/cross_boundary_log.txt` with this format:

```
ws-a-commit: <FEATURE_A_CHANGE_ID>
ws-b-commit: <FEATURE_B_CHANGE_ID>
merge-commit: <MERGE_CHANGE_ID>
conflict-file: src/api.py
resolution: both-endpoints-kept
```

## Important Notes

- Use `jj log --no-graph -r feature-a -T 'change_id.short() ++ "\n"'` to get change IDs
- After rebase, the `feature-b` bookmark may be moved automatically; check with `jj bookmark list`
- Conflict markers in jj look like `<<<<<<<`, `%%%%%%%`, `+++++++` — remove all of them
- Use `jj resolve --list` to see which files have conflicts

## Acceptance Criteria

- `feature-b` ancestry includes `feature-a` (i.e., feature-b is rebased on top of feature-a)
- `src/api.py` at `feature-b` has no conflict markers and contains both `/users` and `/products` endpoints
- `main` bookmark has both `feature-a` and `feature-b` as ancestors
- `/home/user/cross_boundary_log.txt` exists with all 5 required lines

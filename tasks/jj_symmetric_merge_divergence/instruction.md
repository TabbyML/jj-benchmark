# Symmetric Merge Divergence Reconciliation

## Context

You are an OS engineer studying jj's divergence behavior at `/home/user/repo`. The repository has two commits that both describe themselves as `fix: patch` but have different content in `src/patch.py`. This simulates a divergence scenario (two commits with the same logical intent but divergent content).

## Repository State

Use `jj log -r 'description("fix: patch")'` to find the two divergent commits. Both are children of `main` and have:
- **Commit A (patch-v1)**: `src/patch.py` with function `def apply_patch_v1()` and the `patch` bookmark pointing to it
- **Commit B (patch-v2)**: `src/patch.py` with function `def apply_patch_v2()` and no bookmark

## Your Task

### Step 1: Identify the divergent commits

Run:
```
jj log -r 'description("fix: patch")'
```
Note the two change IDs. Examine each one's content.

### Step 2: Reconcile by squashing into a single canonical commit

Use `jj new` to create a merge of both divergent commits, then squash into one:

Option A — Merge then squash:
```
jj new <patch-v1-rev> <patch-v2-rev> -m "fix: patch"
```
Then edit `src/patch.py` to contain BOTH functions:
```python
def apply_patch_v1():
    """Apply patch version 1."""
    return "patch_v1"


def apply_patch_v2():
    """Apply patch version 2."""
    return "patch_v2"


def apply_patch():
    """Apply the canonical patch (combines v1 and v2)."""
    return apply_patch_v1(), apply_patch_v2()
```

### Step 3: Verify single canonical commit

After reconciliation, verify that `jj log -r 'description(exact:"fix: patch")'` returns exactly ONE commit (the reconciled one).

### Step 4: Update the `patch` bookmark

Move the `patch` bookmark to the canonical commit:
```
jj bookmark move patch --to @
```

### Step 5: Write the divergence log

Write `/home/user/divergence_log.txt` with exactly this format:
```
approach: merge_then_edit
patch_v1_change_id: <change_id_of_original_patch_v1>
patch_v2_change_id: <change_id_of_original_patch_v2>
canonical_change_id: <change_id_of_reconciled_commit>
resolution: both functions combined in single commit
```

## Constraints

- The final `src/patch.py` must contain both `def apply_patch_v1()` and `def apply_patch_v2()`
- The `patch` bookmark must exist and point to the reconciled commit
- The log file must use the exact format shown
- No conflict markers in `src/patch.py`

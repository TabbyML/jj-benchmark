# Recover Repo State Using `jj op restore`

You are an OS engineer evaluating how Jujutsu (jj) handles recovery from mistaken operations compared to Git's `git reflog`. The repository is at `/home/user/project`.

## Background

While experimenting with jj, you accidentally ran `jj squash` which merged the tip commit into its parent, losing the tip commit as a standalone revision. In Git you would use `git reflog` and `git reset --hard <sha>` to recover, but in jj the equivalent workflow uses the **operation log** (`jj op log`) and **`jj op restore`**.

Your goal is to understand the operation log, identify the operation that existed **before** the squash was run, and restore the repository to that earlier state — bringing back the lost commit as a standalone revision.

## Starting Environment

- The jj (git-backed) repository is at `/home/user/project`.
- The repo has **two visible commits** above the root:
  1. A commit with description **"add base module"** — adds the file `base.py`.
  2. A commit with description **"refactor: squash target"** — adds the file `refactor.py`. This commit was squashed into its parent in the most recent operation. Its changes are now absorbed into "add base module" and it no longer appears as a separate commit in `jj log`.
- The current working copy (`@`) is an **empty change** on top of the single merged commit.
- The file `refactor.py` is now part of the merged commit, not a separate standalone revision.

## Your Task

You must recover the original two-commit history by using jj's operation log. The workflow mirrors `git reflog` but is fully integrated into jj.

### Step 1: View the Operation Log

Run `jj op log` (alias for `jj operation log`) inside `/home/user/project` to see the history of operations performed on this repository. Each entry shows an operation ID, a timestamp, and a description of what was done.

Look at the operation descriptions. Identify the **most recent operation** (shown at the top) — it will describe a `squash` action. The operation **immediately below it** (its parent) represents the state of the repo **before** the squash happened.

### Step 2: Inspect the Pre-Squash State

Before restoring, verify you have found the correct operation by previewing what the repository looked like at that earlier point. Use:

```
jj --at-op=<OPERATION_ID> log
```

Replace `<OPERATION_ID>` with the ID of the operation that preceded the squash (you can use an unambiguous prefix — typically 8–12 hex characters). When the repo is loaded at that operation, you should see **two distinct commits** in the log: one with description **"add base module"** and one with description **"refactor: squash target"**.

This `--at-op` flag is jj's equivalent of `git show <reflog-sha>` — it lets you inspect the repo at any past operation without modifying anything.

### Step 3: Restore to the Pre-Squash Operation

Now restore the repository to the state at the operation you identified:

```
jj op restore <OPERATION_ID>
```

This command creates a **new operation** that sets the repo state back to what it was at the given operation ID. This is analogous to `git reset --hard <reflog-sha>` but safer — the squash operation is not deleted from the operation log; it is simply no longer the current state.

### Step 4: Verify the Recovery

After running `jj op restore`, confirm the recovery was successful:

1. Run `jj log` and verify **both** commits are now visible as separate revisions:
   - A commit with description **"add base module"**
   - A commit with description **"refactor: squash target"**
2. Check that the file `/home/user/project/refactor.py` exists on disk with content that includes the line `# refactor module`.
3. Run `jj op log` and confirm a new `restore` operation appears at the top of the operation log (the most recent operation).

## Key Differences from Git Reflog

- In Git: `git reflog` shows SHA history; recovery requires `git reset --hard <sha>` or `git checkout <sha>`.
- In jj: `jj op log` shows operation history with human-readable descriptions; recovery uses `jj op restore <op-id>` which is a **non-destructive forward operation** (it does not rewrite history — it adds a new operation on top).
- `jj op restore` is more precise than `jj undo` when you need to jump to a specific operation that is not the most recent one.

## Important Constraints

- Work exclusively with `jj` commands — do **not** use `git` commands.
- The working directory for all commands is `/home/user/project`.
- No root or sudo access is needed.
- Operation IDs are long hex strings; you only need an unambiguous prefix when passing them to `--at-op` or `op restore`.
- The `jj op restore` command accepts a single positional argument: the operation ID.

## Expected Final State

When you are done:
- `jj log` shows **two commits** above the root: **"add base module"** and **"refactor: squash target"**.
- `/home/user/project/refactor.py` exists on disk and contains `# refactor module`.
- `/home/user/project/base.py` exists on disk.
- `jj op log` shows a `restore` operation as the most recent entry at the top.

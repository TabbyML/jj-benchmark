# Recovering an Abandoned Support Ticket Commit in Jujutsu

## Scenario

You are a support engineer at a software company using Jujutsu (`jj`) for version control. Earlier today, while cleaning up your workspace, you accidentally ran `jj abandon` on a commit that contained important work for support ticket #1042 — a bug fix for a null pointer exception in the authentication service.

The repository is located at `/home/user/support-repo`. The abandoned commit had the description `fix: null pointer in auth service (ticket-1042)` and it added a file called `auth_fix.py`. You need to recover this work so you can continue the investigation.

## Background

In Jujutsu, `jj abandon` removes a revision from the visible commit graph, but the commit data is **not immediately deleted**. Abandoned commits can be found and recovered using the operation log.

Jujutsu's operation log (`jj op log`) records every mutation to the repository — including `jj abandon` operations. Each operation has an ID, and you can inspect what the repository looked like at any given operation. This makes Jujutsu extremely safe for exploratory workflows: even destructive-looking commands can be undone.

### Recovery workflow

The standard recovery approach for a single abandoned commit is:

1. **Find the commit** — Use `jj op log` to identify when the abandon happened, then use `jj --at-op=<op-id> log` to confirm the abandoned commit's change ID or commit ID, then use `jj new <change-id>` to bring it back as a parent of a new working-copy commit.

2. **Restore via `jj new <rev>`** — Once you have identified the commit ID (or change ID) of the abandoned commit, run `jj new <commit-id>` to create a new working-copy commit whose parent is the recovered commit. The abandoned commit's content becomes accessible, and `auth_fix.py` will appear in your working copy.

### Key commands

- `jj op log` — Shows the list of operations performed on the repository
- `jj --at-op=<op-id> log` — Shows what `jj log` looked like immediately after a specific operation
- `jj --at-op=<op-id> log --no-graph -T 'commit_id.short() ++ " " ++ description'` — Useful to extract the commit ID of the abandoned commit
- `jj new <rev>` — Creates a new empty working-copy commit as a child of `<rev>`

## Repository Setup

The repository at `/home/user/support-repo` has been pre-configured with:

- A `jj` repository initialised at `/home/user/support-repo`
- A commit with description `initial project setup` with a `main` bookmark pointing to it
- A commit with description `fix: null pointer in auth service (ticket-1042)` that adds the file `auth_fix.py` — **this commit has already been abandoned**
- The current working copy (`@`) is an empty commit whose parent is the `initial project setup` commit

## Your Task

You must recover the abandoned commit so that:

1. The commit `fix: null pointer in auth service (ticket-1042)` becomes the **parent** of the current working-copy commit (`@`)
2. The file `auth_fix.py` is present and accessible in the working copy
3. The `main` bookmark still points to `initial project setup`

## Steps

### Step 1 — Examine the current state

Run `jj log` to see what commits are currently visible. You will notice that the `fix: null pointer in auth service (ticket-1042)` commit is **not** shown — it has been abandoned.

Run `jj status` to see the current working-copy state.

### Step 2 — Browse the operation log

Run `jj op log` to see the history of operations on this repository. Each entry has an operation ID, timestamp, and description. Look for an entry that says something like `abandon commit` — that is when the commit was removed.

Note the operation ID of the operation **immediately before** the abandon (the second entry, or the parent of the abandon operation).

### Step 3 — Find the abandoned commit's ID

Use `jj --at-op=<op-id> log --no-graph -T 'commit_id.short() ++ " " ++ description'` with the pre-abandon operation ID to see what the log looked like before the abandon. This will show you the commit ID (or change ID) of `fix: null pointer in auth service (ticket-1042)`.

Copy that commit ID (the short form is fine).

### Step 4 — Restore the abandoned commit as a parent

Run:

```
jj new <commit-id>
```

Replace `<commit-id>` with the short commit ID you found in Step 3. This creates a new empty working-copy commit whose parent is the previously abandoned commit. The abandoned commit is now visible in `jj log` again, and its file contents are accessible.

### Step 5 — Verify the recovery

Run `jj log` — you should see `fix: null pointer in auth service (ticket-1042)` in the history.

Run `jj show @-` — the parent of your working copy should show `fix: null pointer in auth service (ticket-1042)` with the changes to `auth_fix.py`.

Verify the file exists: `ls auth_fix.py` (from within `/home/user/support-repo`).

## Important Notes

- Work exclusively in `/home/user/support-repo`; do **not** use `git` commands
- You do **not** need root/sudo
- The `jj op log` output lists operations newest-first; the second entry (or first non-current entry) is the state before the abandon
- `jj --at-op=<op-id>` allows you to inspect the repository as it was at that operation without modifying anything
- Shorthand: `jj op log` → identify pre-abandon op-id → `jj --at-op=<op-id> log` to get commit ID → `jj new <commit-id>` to recover

## Expected Final State

- `jj log` shows `fix: null pointer in auth service (ticket-1042)` as a visible (non-abandoned) commit
- The working-copy commit `@` has `fix: null pointer in auth service (ticket-1042)` as its direct parent
- The file `/home/user/support-repo/auth_fix.py` exists
- The `main` bookmark still points to `initial project setup`

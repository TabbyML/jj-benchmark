# CI Release Bookmark Workflow

## Context

You are a build/release engineer maintaining a CI pipeline for a project stored in a `jj` (Jujutsu) repository. The repository is located at `/home/user/project`. The repo already has a short history: a root commit, then three sequential feature commits stacked on top of each other.

The three commits are described as:
1. `feat: add authentication module` — introduces `src/auth.py`
2. `feat: add payment processing` — introduces `src/payment.py`
3. `feat: add notification service` — introduces `src/notify.py`

All three commits are currently mutable (not immutable/tagged). The working copy (`@`) sits on top of commit 3 as an empty change.

## Your Assignment

You need to prepare this repository for a `v1.0` release using `jj` commands only. The release workflow requires the following steps, which you must perform **in order**:

### Step 1 — Squash the three feature commits into a single release commit

The three sequential feature commits (`feat: add authentication module`, `feat: add payment processing`, `feat: add notification service`) must be combined into one commit. The final squashed commit must include all three source files (`src/auth.py`, `src/payment.py`, `src/notify.py`) and must have the description:

```
release: v1.0 — bundle auth, payment, and notification
```

The working copy (`@`) should remain as an empty commit on top of this squashed commit after the squash operation.

**Hint:** Think about how to squash a range of commits into one. You will need to work from the bottom of the stack upward. Using `jj log` to inspect the current state before acting is a good first step. You can refer to revisions by their description or by walking the parent chain from `@`.

### Step 2 — Create a bookmark named `release/v1.0` pointing at the squashed commit

Once you have a single squashed release commit, create a bookmark named `release/v1.0` that points **at the squashed release commit** (the parent of the current working copy, i.e. `@-`).

Bookmarks in `jj` are created with `jj bookmark create`. Make sure the bookmark targets the correct revision.

### Step 3 — Set a tag named `v1.0` on the squashed release commit

In addition to the bookmark, create a tag named `v1.0` pointing at the same squashed release commit (`@-`).

Tags in `jj` are managed with `jj tag set`.

### Step 4 — Verify the final state

After completing the steps above, run `jj log` and `jj bookmark list` to confirm:

- There is exactly **one non-root, non-working-copy mutable commit** in the history (the squashed release commit).
- The squashed commit has the description `release: v1.0 — bundle auth, payment, and notification`.
- The squashed commit contains the files `src/auth.py`, `src/payment.py`, and `src/notify.py`.
- A bookmark named `release/v1.0` exists and points to the squashed commit.
- A tag named `v1.0` exists and points to the squashed commit.
- The working copy (`@`) is an empty commit that is a child of the squashed commit.

## Starting Environment Assumptions

- Home directory: `/home/user`
- The `jj` repository is at `/home/user/project`
- `jj` is installed and on `$PATH`
- `git` is installed (the repo is a jj-git-backed repo)
- User identity is pre-configured: `user.name = "CI Bot"`, `user.email = "ci@example.com"`
- There are exactly three feature commits stacked linearly above the root commit
- The working copy is empty and sits on top of the third feature commit
- No bookmarks or tags exist at the start

## Important Notes

- Do **not** use `git` commands directly. All operations must use `jj`.
- Do **not** use `sudo`.
- The bookmark name must be exactly `release/v1.0` (with a forward slash).
- The tag name must be exactly `v1.0`.
- The squashed commit description must be exactly: `release: v1.0 — bundle auth, payment, and notification` (note the em dash `—`).
- All three source files must be present in the squashed commit's tree.

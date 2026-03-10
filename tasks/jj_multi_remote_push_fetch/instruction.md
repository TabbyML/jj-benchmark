# Push a Release Bookmark to One Remote and Fetch Updates from Another

You are a build/release engineer maintaining a CI pipeline for a project that uses **Jujutsu (jj)** as its version-control system. Your team uses two separate Git remotes:

- **`origin`** — the authoritative production remote (a local bare Git repo at `/home/user/remotes/origin.git`).
- **`upstream`** — a shared upstream remote from which the team fetches integration work (a local bare Git repo at `/home/user/remotes/upstream.git`).

The working repository is already initialized at `/home/user/myrepo`. It has both remotes configured, a small commit history, and an `upstream` remote that already contains a bookmark called `integration` pointing to a newer commit that does **not** yet exist in your local repo.

## Your Task

Complete all of the following steps **in order** inside `/home/user/myrepo`:

### Step 1 — Create a `release/1.0` bookmark

Create a local bookmark named **`release/1.0`** pointing at the commit whose description is **`"feat: add release notes"`**.

Use:
```
jj bookmark create release/1.0 -r <revset-that-identifies-that-commit>
```

Hint: You can use `jj log` to find the commit, then target it by its change ID or use `description("feat: add release notes")` as the revset.

### Step 2 — Push `release/1.0` to `origin`

Push the `release/1.0` bookmark to the remote named **`origin`**:

```
jj git push --remote origin --bookmark release/1.0
```

After this step, `jj git remote list` should show `origin` and `upstream`, and the bookmark `release/1.0@origin` should exist in your repo's remote-tracking state.

### Step 3 — Fetch the `integration` bookmark from `upstream`

Fetch all bookmarks from the **`upstream`** remote:

```
jj git fetch --remote upstream
```

After the fetch, a remote-tracking bookmark `integration@upstream` should appear in `jj bookmark list --all-remotes`.

### Step 4 — Track and create a local `integration` bookmark

Make the fetched `integration@upstream` bookmark tracked so that a local `integration` bookmark is created/updated:

```
jj bookmark track integration --remote upstream
```

Verify with:
```
jj bookmark list
```

You should see a local bookmark `integration` pointing to the same commit as `integration@upstream`.

### Step 5 — Verify final state

Run the following verification commands and confirm the output matches expectations:

```bash
# Should list both remotes
jj git remote list

# Should show: release/1.0 pointing to the release-notes commit, and integration pointing to the upstream commit
jj bookmark list
```

## Starting Environment

- `/home/user/myrepo` — a jj (git-backend) repo with two configured remotes:
  - `origin` → `/home/user/remotes/origin.git` (bare git repo, starts empty)
  - `upstream` → `/home/user/remotes/upstream.git` (bare git repo, pre-populated with an `integration` bookmark at a commit with description `"ci: add integration pipeline"`)
- The local repo has **three commits** on a linear history (from oldest to newest):
  1. `"init: project scaffold"` — first commit
  2. `"feat: add release notes"` — second commit ← this is your push target
  3. An empty working-copy commit (the current `@`)
- The user config for jj is set (name and email) so no prompts are needed.

## Expected Final State (Truth)

- `jj git remote list` output contains both `origin` and `upstream`.
- `jj bookmark list` (or `jj bookmark list --all-remotes`) shows:
  - A local bookmark `release/1.0` that has been pushed to `origin` (i.e., `release/1.0@origin` exists and matches the local `release/1.0`).
  - A local bookmark `integration` that tracks `integration@upstream` and points to the commit with description `"ci: add integration pipeline"`.
- The commit with description `"ci: add integration pipeline"` exists in the local repo's object store (visible via `jj log -r 'description("ci: add integration pipeline")'`).

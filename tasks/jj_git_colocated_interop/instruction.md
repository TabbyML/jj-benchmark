# jj Git Colocated Interoperability Checkpoints

## Background

You are an OS engineer evaluating Jujutsu (`jj`) as a drop-in workflow alongside Git. A colocated repository lets you run both `jj` and `git` commands in the same directory — `jj` stores its metadata in `.jj/` while Git keeps its `.git/` directory at the root, and the two stay synchronized automatically.

In this task you will take an **existing pure-Git repository**, layer `jj` on top of it using `jj git init --colocate`, build a small commit history, create a bookmark (jj's equivalent of a Git branch), verify that the bookmark is visible as a Git branch via `git`, then delete the bookmark in jj and confirm that Git also reflects the deletion.

The starting environment contains:
- A directory `/home/user/gitrepo` that is already a plain Git repository with two commits: `initial commit` (adding `README.md`) and `add config` (adding `config.toml`).
- The Git `HEAD` points to the `main` branch.

---

## Your Tasks

### 1. Initialize jj in colocated mode

Change into `/home/user/gitrepo` and initialize a jj repository in **colocated** mode so that both `jj` and `git` commands work inside the same directory.

After initialization, confirm that:
- A `.jj/` directory now exists inside `/home/user/gitrepo`.
- `jj status` exits successfully (exit code 0).
- `jj log` shows the two existing commits inherited from Git.

### 2. Configure jj user identity

Set the jj user identity at the **repo level** using `jj config set`:
- `user.name` → `"OS Engineer"`
- `user.email` → `"os@example.com"`

These must be set with the `--repo` flag so they apply only to this repository.

### 3. Create a new commit

Using only jj commands:
1. Create a new file `/home/user/gitrepo/notes.txt` with the single line `interop test`.
2. Describe (commit) the current working-copy change with the message `"add notes"`.

Verify that `jj log` now shows a third commit with description `add notes`.

### 4. Create a jj bookmark and verify it appears as a Git branch

1. Create a bookmark named `feature/interop` pointing to the current working-copy commit (`@`) using `jj bookmark create`.
2. Run `jj git export` to push jj's state into the underlying Git repository.
3. Verify the bookmark appears as a Git branch by running:
   ```
   git -C /home/user/gitrepo branch
   ```
   The branch `feature/interop` must appear in that output.

### 5. Move the bookmark forward

1. Create another new file `/home/user/gitrepo/notes2.txt` with the content `second note`.
2. Commit the working-copy change with `jj commit -m "add notes2"`.
3. Move the `feature/interop` bookmark so that it now points to the new working-copy commit (`@-` is the just-committed change; you want to point at `@-` which is the commit you just finalized with `jj commit`).
   - Use `jj bookmark move feature/interop --to @-`.
4. Export to Git again with `jj git export`.
5. Verify with `git -C /home/user/gitrepo log --oneline feature/interop` that the branch tip has description `add notes2`.

### 6. Delete the bookmark in jj and confirm Git reflects the deletion

1. Delete the `feature/interop` bookmark with `jj bookmark delete feature/interop`.
2. Export to Git with `jj git export`.
3. Confirm that the branch no longer appears in `git -C /home/user/gitrepo branch`.

---

## Verification conditions

At the end of the task, the following must all be true:

1. `/home/user/gitrepo/.jj` directory exists (colocated repo was initialized).
2. Running `jj log -r 'description("add notes2")' --no-graph -T 'description'` inside `/home/user/gitrepo` prints `add notes2`.
3. The file `/home/user/gitrepo/notes.txt` exists and contains the line `interop test`.
4. The file `/home/user/gitrepo/notes2.txt` exists and contains the line `second note`.
5. The bookmark `feature/interop` does **not** exist in jj (deleted): `jj bookmark list` should not include `feature/interop`.
6. The Git branch `feature/interop` does **not** exist: `git branch` inside the repo should not list it.
7. The jj repo-level config has `user.name = "OS Engineer"` (verifiable via `jj config get --repo user.name`).

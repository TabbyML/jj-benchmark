### 1. Library Overview
* **Description**: `jj` (Jujutsu) is a modern, Git-compatible version control system (VCS) designed for speed, safety, and a superior developer experience. It simplifies the Git model by treating the working copy as a permanent commit, eliminating the staging area, and providing "first-class" conflict management where conflicts can be committed and resolved later.
* **Ecosystem Role**: It acts as a powerful alternative CLI for Git repositories. It uses a Git backend by default, allowing developers to use `jj` locally while interacting with standard Git remotes (GitHub, GitLab, etc.). It competes with tools like `git-branchless` and `sl` (Sapling).
* **Installation**: jj could be installed by following command:

```bash
curl -fsSL \
    https://github.com/jj-vcs/jj/releases/download/v0.38.0/jj-v0.38.0-x86_64-unknown-linux-musl.tar.gz | \
    tar -xz -C /usr/local/bin ./jj && \
    chmod +x /usr/local/bin/jj
```

* **Project Setup**:
    * **Initialize a new Git-compatible repo**: `jj git init --colocate` (creates a `.jj` directory alongside a `.git` directory in the current folder).
    * **Clone an existing repo**: `jj git clone <url>` (clones a Git repo and initializes it for `jj`).
    * **Identity configuration**: `jj config set --user user.name "Your Name"` and `jj config set --user user.email "your@email.com"`.
### 2. Core Primitives & APIs* **Working Copy as Commit (`@`)**: In `jj`, the working copy is always a commit. Any file change is automatically recorded in the current commit when you run any `jj` command.
    * [Working Copy Docs](https://docs.jj-vcs.dev/latest/tutorial/#the-working-copy)
* **Change ID vs. Commit ID**: A **Change ID** (e.g., `qpvz`) is stable and persists across rebases/rewrites. A **Commit ID** (Git SHA, e.g., `a1b2c3d4`) changes whenever the commit content or parent changes.
    * [Change/Commit IDs](https://docs.jj-vcs.dev/latest/tutorial/#commit-ids-and-change-ids)
* **Revsets**: A functional query language for selecting revisions.
    * `jj log -r '@-'` (Parent of working copy)
    * `jj log -r 'main..@'` (Commits in current branch not in main)
    * `jj log -r 'author("Alice") & description("fix")'` (Search by author and message)
    * [Revset Reference](https://docs.jj-vcs.dev/latest/revsets/)
* **Operation Log & Undo**: Every repository operation (commit, rebase, push) is recorded and can be reverted.
    * `jj op log` (View history of operations)
    * `jj undo` (Undo the last operation)
    * [Operation Log Docs](https://docs.jj-vcs.dev/latest/operation-log/)
* **First-class Conflicts**: Conflicts are stored in the commit graph. You can rebase a commit with conflicts, and the conflicts will propagate to descendants until resolved.
    * `jj resolve` (Tools to help resolve conflicts)
    * [Conflict Management](https://docs.jj-vcs.dev/latest/conflicts/)
### 3. Real-World Use Cases & Templates
* **Stacking Changes for PRs**: `jj` makes it easy to manage a "stack" of small commits. You can edit any commit in the stack with `jj edit <change_id>`, and all descendants will automatically rebase.
* **GitHub Workflow**: `jj` integrates with GitHub via bookmarks (branches). To push a PR:
    1. `jj bookmark create my-feature`
    2. `jj git push`
* **Templates**: Customize output formatting (e.g., for `jj log`).
    * `jj log -T 'commit_id.short() ++ " " ++ description.first_line()'`
    * [Template Language](https://docs.jj-vcs.dev/latest/templates/)
### 4. Developer Friction Points
* **Pushing requires Bookmarks**: Unlike Git, where you are always "on" a branch, `jj` allows "anonymous" commits. New users often forget to create a bookmark before trying to `jj git push`, leading to "nothing to push" errors.
* **Conflict Markers in Commits**: Users might accidentally commit conflict markers (`<<<<<<<`) if they don't realize that `jj` allows committing "unresolved" states. Understanding that a commit *with* conflicts is valid but "broken" is a mental shift.
* **Revset Syntax Complexity**: Distinguishing between `..` (range) and `::` (DAG range/ancestors) can be tricky for beginners.
### 5. Evaluation Ideas
* **Conflict Resolution**: Perform a rebase that creates a conflict, then resolve it by editing the file and observe the automatic "resolution" in the next `jj st`.
* **History Rewriting**: Use `jj edit` on a commit 3 levels deep in a stack, change a file, and verify all 3 descendant commits were automatically rebased.
* **Operation Recovery**: Accurately describe the state of the repo after performing 5 distinct operations, then use `jj undo` to return to the state after the 2nd operation.
* **Revset Querying**: Write a revset to find all commits authored by "Bob" that are not reachable from the `main` bookmark but are ancestors of the current working copy.
* **Commit Splitting**: Use `jj split` to take a single commit with changes in two different files and turn it into two separate commits.
* **Git Integration**: Successfully clone a Git repo, create a bookmark, and push it to a remote using only `jj` commands.
### 6. Sources
1. [Jujutsu Official Documentation](https://docs.jj-vcs.dev/latest/) - Primary source for all concepts and commands.
2. [Jujutsu GitHub Repository](https://github.com/jj-vcs/jj) - Source for issue tracking and architecture details.
3. [Jujutsu Tutorial (Bird's Eye View)](https://docs.jj-vcs.dev/latest/tutorial/) - Step-by-step guide for new users.
4. [Revset Language Reference](https://docs.jj-vcs.dev/latest/revsets/) - Detailed syntax for the query language.
5. [GitHub Discussions (Common Issues)](https://github.com/jj-vcs/jj/discussions) - Source for developer friction points and UX challenges.

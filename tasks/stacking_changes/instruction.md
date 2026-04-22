# Stacking Changes with Jujutsu (jj)

## Background
Jujutsu (`jj`) is a modern version control system that treats the working copy as a permanent commit and makes it easy to manage a "stack" of small commits. You can edit any commit in the stack with `jj edit <change_id>`, and all descendants will automatically rebase.

## Requirements
In the repository at `/home/user/repo`, there is a linear history of commits on top of the initial commit:
1. Commit with description "Add feature 1" (adds `feature1.txt`)
2. Commit with description "Add feature 2" (adds `feature2.txt`)
3. Commit with description "Add feature 3" (adds `feature3.txt`)

Your task is to modify the commit "Add feature 1" to also include a new file `feature1-docs.txt` with the exact content `Docs for feature 1`, without breaking the descendants. The final working copy must be at the tip of the stack (the descendant of "Add feature 3").

## Implementation
1. Go to the project directory `/home/user/repo`.
2. Use `jj log` to find the change ID of the commit with description "Add feature 1".
3. Use `jj edit <change_id>` to edit that commit.
4. Create the file `feature1-docs.txt` with the content `Docs for feature 1`.
5. Use `jj log` to find the change ID of the commit "Add feature 3".
6. Use `jj edit <change_id>` or `jj new <change_id>` to return to the tip of the stack.

## Constraints
- Project path: `/home/user/repo`
- The repository is a `jj` repository.
- You must not abandon any of the three commits.
- The content of `feature1-docs.txt` must be exactly `Docs for feature 1`.
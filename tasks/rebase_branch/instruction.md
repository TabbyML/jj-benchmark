# Rebase a Bookmark and Resolve Conflicts in jj

## Background
Jujutsu (`jj`) is a Git-compatible VCS that treats the working copy as a permanent commit and has first-class conflict management. In this task, you will rebase a bookmark (branch) onto `main` and resolve a conflict.

## Requirements
- You have an initialized `jj` repository at `/home/user/repo`.
- The `main` bookmark has been updated with a new commit modifying `data.txt`.
- You have a bookmark `feature-branch` with 2 commits. The first commit modifies `data.txt` in a way that conflicts with `main`.
- Rebase `feature-branch` onto `main`.
- Resolve the conflict in `data.txt` by keeping both lines (the line from `main` followed by the line from `feature-branch`).
- The `feature-branch` bookmark must point to the head of the rebased commits.

## Implementation
1. Navigate to `/home/user/repo`.
2. Rebase the commits of `feature-branch` onto `main`.
3. Identify the conflicted file (`data.txt`).
4. Edit `data.txt` to resolve the conflict. The final file should contain:
   ```
   Line from main
   Line from feature
   ```
5. Verify the conflict is resolved. You can use `jj resolve` to mark it as resolved or edit the file directly.

## Constraints
- Project path: `/home/user/repo`
- Do not create any new bookmarks.
- The final `data.txt` in the `feature-branch` must have exactly the two lines specified.
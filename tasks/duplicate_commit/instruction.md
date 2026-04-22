# Duplicate a Commit in Jujutsu

## Background
You are working in a Jujutsu repository and have developed a feature on one branch, but you realize you also need the exact same changes applied on top of another branch. Instead of manually rewriting the changes, you can duplicate the commit.

## Requirements
- You have a Jujutsu repository located at `/home/user/repo`.
- There are two branches (bookmarks): `feature-a` and `feature-b`.
- You need to duplicate the commit pointed to by `feature-a` so that the new duplicated commit is placed directly on top of `feature-b` (i.e., its parent is `feature-b`).
- Do not modify the original `feature-a` commit.

## Implementation Guide
1. Navigate to the repository at `/home/user/repo`.
2. Use the `jj duplicate` command to copy the commit at `feature-a` and set its destination to `feature-b`.

## Constraints
- Project path: `/home/user/repo`
- Use only `jj` commands.
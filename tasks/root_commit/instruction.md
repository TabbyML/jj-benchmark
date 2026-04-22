# Create a New Root Commit in Jujutsu

## Background
In Jujutsu (`jj`), every repository has a virtual `root()` commit that is the oldest ancestor of all other commits. Creating a new commit directly on top of the root commit is useful for starting a new branch without any history (similar to an orphan branch in Git).

## Requirements
- You have a Jujutsu repository at `/home/user/myproject`.
- Create a new, empty change that is a direct child of the `root()` commit.
- The working copy (`@`) must be updated to point to this newly created commit.

## Implementation
1. Navigate to `/home/user/myproject`.
2. Run a single `jj` command to create a new commit that uses the `root()` revset as its parent.

## Constraints
- Project path: `/home/user/myproject`
- Only use `jj` commands.
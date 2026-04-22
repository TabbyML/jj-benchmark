# Export to Backing Git Repo

## Background
Jujutsu (`jj`) can be used as a front-end for an existing Git repository without being colocated (i.e., keeping the `.jj` and `.git` directories separate). In this setup, changes made in Jujutsu are not automatically reflected in the underlying Git repository until they are explicitly exported.

## Requirements
You have a Git repository at `/home/user/git-repo` and a separate Jujutsu repository at `/home/user/jj-repo` which uses the Git repository as its backing store.
A new bookmark `feature-x` has been created and committed in `/home/user/jj-repo`, but it is not yet visible as a branch in `/home/user/git-repo`.
Your task is to export the Jujutsu bookmarks to the backing Git repository so that the `feature-x` branch becomes available in `/home/user/git-repo`.

## Implementation
1. Navigate to the Jujutsu repository.
2. Run the appropriate command to update the underlying Git repository with changes made in the Jujutsu repository.

## Constraints
- Do not modify the repositories' locations.
- Project paths: `/home/user/git-repo` and `/home/user/jj-repo`
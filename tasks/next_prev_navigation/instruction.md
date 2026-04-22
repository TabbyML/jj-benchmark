# Navigate history with jj next and prev

## Background
Jujutsu (`jj`) allows you to easily navigate the commit graph using the `jj next` and `jj prev` commands. These commands change the parent of the working-copy commit to a child or ancestor revision, effectively letting you move up and down the history tree without checking out branches in the traditional Git sense.

## Requirements
You have a repository located at `/home/user/myproject` with a linear history of commits: `A` -> `B` -> `C` -> `D`. Currently, the working copy is a new empty commit that is a child of commit `D`.

1. Move the working copy to be a child of commit `C` using `jj prev`.
2. From there, move the working copy to be a child of commit `A` using `jj prev` with an offset.
3. Finally, move the working copy forward to be a child of commit `B` using `jj next`.

## Constraints
- **Project path**: /home/user/myproject
- The final working copy commit must be an empty commit whose parent is commit `B`.
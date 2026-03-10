You are a developer migrating from Git who wants to experiment with a feature branch without modifying the original commits. The repository has a `feature` branch with a commit that adds a new function to `app.py`. 

Your task is to:
1. Duplicate the commit pointed to by the `feature` bookmark.
2. Rebase the duplicated commit so that it is a child of the `main` bookmark.
3. Create a new bookmark called `feature-experiment` pointing to this newly duplicated and rebased commit.
4. Leave the original `feature` bookmark and its commit unchanged.

To verify your work, the `feature-experiment` bookmark must point to a commit that has the same exact changes as `feature`, but its parent must be the commit pointed to by `main`.

# Absorb Changes into Appropriate Commits

## Background
You are working on a project tracked with `jj` (Jujutsu) at `/home/user/project`. 
You have been developing two distinct features in a stack of commits:
1. A commit that modifies `feature_a.py`.
2. A child commit that modifies `feature_b.py`.

While testing the latest state, you found bugs in both features and fixed them directly in your current working copy (`@`). Instead of manually splitting these changes and squashing them into their respective commits, you want to use a single `jj` command to automatically distribute these bug fixes to the appropriate mutable ancestors where the lines were last modified.

## Requirements
- Distribute the changes in your working copy to the nearest mutable ancestors using the appropriate `jj` command.
- After the operation, the working copy (`@`) should be empty (no changes).

## Implementation Guide
1. Navigate to `/home/user/project`.
2. Run the `jj absorb` command to automatically move the changes from the working copy into the appropriate ancestor commits.
3. Verify that the changes to `feature_a.py` were absorbed into the commit that originally modified `feature_a.py`.
4. Verify that the changes to `feature_b.py` were absorbed into the commit that originally modified `feature_b.py`.

## Constraints
- Project path: `/home/user/project`
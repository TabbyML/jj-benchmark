# Insert a New Commit in a jj Stack

## Background
You have a `jj` repository with a stack of commits at `/home/user/myproject`. The commit graph looks like this: `A` -> `B` -> `C`. You need to insert a new commit between `A` and `B` without breaking the descendants.

## Requirements
- Insert a new commit that is a child of the commit with the description "commit A" and a parent of the commit with the description "commit B".
- The new commit must contain a new file named `feature.txt` with the exact text `new feature\n`.
- The descendants (`B` and `C`) must be rebased on top of this new commit.
- The working copy should be left at the tip of the stack (the new version of `C`).

## Implementation Guide
1. Go to `/home/user/myproject`.
2. Find the Change ID or Revision of "commit A".
3. Start a new commit off of "commit A" using `jj new <commit_A_id>`.
4. Create `feature.txt` with the text `new feature\n`.
5. Rebase the sub-tree starting at "commit B" onto your new commit using `jj rebase -s <commit_B_id> -d @`.
6. Move your working copy back to the new version of "commit C" using `jj new <commit_C_id>` or `jj edit <commit_C_id>`.

## Constraints
- Project path: `/home/user/myproject`
- Do not modify the contents of the existing commits `A`, `B`, or `C`.
- The final stack should be `A` -> `New Commit` -> `B'` -> `C'`.
# Rewrite History in a Jujutsu Stack

## Background
`jj` (Jujutsu) makes it easy to manage a "stack" of small commits. You can edit any commit in the stack with `jj edit <change_id>`, and all descendants will automatically rebase.

## Requirements
- You have a `jj` repository at `/home/user/repo` with a linear stack of 4 commits: Base -> Commit 1 -> Commit 2 -> Commit 3.
- The Base commit has a file `base.txt` with content `old`.
- Edit the Base commit so that `base.txt` contains `new`.
- Observe that Commits 1, 2, and 3 are automatically rebased.
- You must end up with the same 4 commit structure, but with the modified base.

## Implementation
1. Go to `/home/user/repo`.
2. Identify the change ID of the "Base" commit.
3. Run `jj edit <change_id>` to edit it.
4. Change the content of `base.txt` to `new`.
5. Run `jj new` to finalize the edit, or simply check the status.

## Output
- Project path: `/home/user/repo`
- Start command: `cd /home/user/repo`
- Port: N/A
# Abandoning Commits in Jujutsu

## Background
You are working in a `jj` repository and have created a stack of commits. You've realized that some of the intermediate commits are false starts and need to be removed from the history. `jj abandon` allows you to discard revisions and automatically rebases any descendants.

## Repository State
- `commit A`: adds `a.txt`. Bookmark: `feature-a`.
- `commit B`: adds `b.txt`. Bookmark: `experiment`.
- `commit C`: adds `c.txt`. Bookmark: `draft`.
- `commit D`: adds `d.txt`. Working copy is here.

## Requirements
1. Abandon the commit pointed to by the `experiment` bookmark, but **retain** the bookmark (it should automatically move to the abandoned commit's parent).
2. Abandon the commit pointed to by the `draft` bookmark. Do **not** retain this bookmark (it should be deleted).
3. Set the description of the current working-copy commit to `cleanup complete`.

## Constraints
- Project path: `/home/user/myproject`
- Use only `jj` commands.
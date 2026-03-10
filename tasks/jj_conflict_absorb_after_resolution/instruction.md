You are a developer working in a jj repository at `/home/user/repo`. After resolving a conflict, you have uncommitted fixes in the working copy. You need to absorb those working copy changes back into the appropriate parent commit.

Starting state:
- `base` bookmark: commit `base: add module` with `module.py` containing `VALUE = 1`
- `main` bookmark: commit `main: update value to 10` with `module.py` containing `VALUE = 10`
- `feature` bookmark: commit `feat: update value to 20` (from base) with `module.py` containing `VALUE = 20`
- `feature` has been rebased onto `main`, creating a conflict in `module.py`
- The working copy (`@`) is above the conflicted `feature` commit

Your tasks:

1. Check conflicts: `jj resolve --list > /home/user/repo/before_absorb.txt`
2. Resolve the conflict: edit `module.py` in the `feature` commit to contain `VALUE = 20\nPARENT_VALUE = 10\n`
   (Use `jj edit feature` to navigate to the conflicted commit, fix it, then `jj edit @+` to return)
3. Update description: `jj describe -m "feat: update value to 20 (resolved)"` on the feature commit
4. Navigate back: `jj new feature` to create a new working copy on top
5. Make an additional small fix in the working copy: `echo 'EXTRA = True' >> /home/user/repo/module.py`
6. Absorb the working copy change: `jj absorb`
7. Save the final state: `jj log --no-graph -T 'description ++ "\n"' -r 'all()' > /home/user/repo/after_absorb.txt`

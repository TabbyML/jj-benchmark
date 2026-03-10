You are a contributor preparing a set of changes for upstream submission using the `jj` version control CLI. You have been working in a repository at `/home/user/repo` on a feature but your commits are a bit messy. The repository has a `main` branch and you are working on a bookmark named `feature`. 

Currently, there are three commits on your bookmark:
1. The first commit adds a new file `utils.py` with some helper functions.
2. The second commit accidentally modifies both `utils.py` (fixing a bug) and adds a new file `api.py` (a new feature) in the same commit.
3. The third commit adds tests for `api.py` in `test_api.py`.

Your task is to clean up this history for review:
1. First, you need to `jj split` the second commit so that the bug fix to `utils.py` is in its own commit, and the addition of `api.py` is in another commit.
2. Then, you need to `jj squash` the bug fix commit for `utils.py` into the first commit (the one that originally added `utils.py`).
3. After that, ensure that the `api.py` commit and the `test_api.py` commit remain as separate, subsequent commits on top of the squashed `utils.py` commit.
4. Finally, make sure the `feature` bookmark points to the final commit (`test_api.py`).

When you are done, run `jj log -r 'main..feature' -T 'description ++ "
"' --no-graph > /home/user/result.txt` to save the final commit descriptions in order (from newest to oldest).

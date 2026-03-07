You are a support engineer recovering lost work for a developer. They abandoned a branch named `feature-x` and now need to recover it and rebase it onto the `main` branch. 
Your task is to:
1. Find the abandoned revision that was previously pointed to by `feature-x`.
2. Restore the bookmark `feature-x` to point to that revision.
3. Rebase `feature-x` onto the `main` branch.
4. Save the output of `jj log -r feature-x` to `/home/user/log.txt`.

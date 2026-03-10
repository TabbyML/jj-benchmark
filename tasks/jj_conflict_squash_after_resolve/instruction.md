You are a developer working in a jj repository at `/home/user/repo`. After a rebase, `data.json` has a conflict. Once you resolve it, you should squash the resolved commit into its parent.

Starting state:
- `base` bookmark: commit `base: init data` with `data.json` containing `{"value": 0}`
- `main` bookmark: commit `main: set value 10` with `data.json` containing `{"value": 10}`
- `feature` bookmark: commit `feat: set value 20` (branched from base) with `data.json` containing `{"value": 20}`
- `feature` has been rebased onto `main`, creating a conflict in `data.json`
- The working copy (`@`) is an empty commit above the conflicted `feature` commit

Your tasks:

1. Check the conflict: `jj resolve --list`
2. Resolve the conflict in `data.json` by editing it to contain exactly: `{"value": 20, "merged": true}\n`
3. Run `jj describe -m "feat: set value 20 (resolved)"` on the feature commit
4. Squash the resolved feature commit into main by running `jj squash --from feature --into main`
5. Save the final log to `/home/user/repo/final_log.txt`: `jj log --no-graph -T 'description ++ "\n"' -r 'all()' > /home/user/repo/final_log.txt`

After squashing, the `main` bookmark commit should contain `data.json` with `{"value": 20, "merged": true}`.

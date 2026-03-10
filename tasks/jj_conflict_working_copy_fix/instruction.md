You are a developer working in a jj repository at `/home/user/repo`. You have uncommitted changes in the working copy (`@`) that conflict with a recent rebase of the parent commit.

Starting state:
- `base` bookmark: commit `base: add env` with `env.sh` containing `ENV=base`
- `main` bookmark: commit `main: set ENV=prod` with `env.sh` containing `ENV=prod`
- Working copy (`@`): has uncommitted edit to `env.sh` containing `ENV=dev` on top of `base`, but the parent was rebased onto `main` creating a conflict
- The working copy itself has a conflict in `env.sh`

Your tasks:

1. Check the current working copy conflict status: `jj status > /home/user/repo/wc_status.txt`
2. List conflicted files: `jj resolve --list > /home/user/repo/wc_conflicts.txt`
3. Fix the conflict in `env.sh` by editing it to contain: `ENV=prod\nDEV_OVERRIDE=true\n`
4. Save the resolved status: `jj status > /home/user/repo/wc_status_after.txt`
5. Describe the working copy: `jj describe -m "wc: set ENV with dev override"`
6. Verify clean: `jj resolve --list > /home/user/repo/wc_conflicts_after.txt`

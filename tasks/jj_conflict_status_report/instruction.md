You are a developer working in a jj repository at `/home/user/repo`. A rebase has created a conflict in `service.yaml`. You need to document the conflict state before and after resolution.

Starting state:
- `base` bookmark: commit `base: add service config` with `service.yaml` containing `replicas: 1`
- `main` bookmark: commit `main: scale to 3` with `service.yaml` containing `replicas: 3`
- `feature` bookmark: commit `feat: scale to 5` (branched from base) with `service.yaml` containing `replicas: 5`
- `feature` has been rebased onto `main`, creating a conflict in `service.yaml`

Your tasks:

1. Capture the pre-resolution status:
   - `jj status > /home/user/repo/status_before.txt`
   - `jj resolve --list > /home/user/repo/conflicts_before.txt`
   - `jj log --no-graph -T 'change_id.short() ++ " " ++ description ++ "\n"' -r 'all()' > /home/user/repo/log_before.txt`

2. Resolve the conflict: edit `service.yaml` to contain exactly `replicas: 5\nstrategy: RollingUpdate\n`

3. Update description: `jj describe -m "feat: scale to 5 (resolved)"`

4. Capture the post-resolution status:
   - `jj status > /home/user/repo/status_after.txt`
   - `jj resolve --list > /home/user/repo/conflicts_after.txt`
   - `jj log --no-graph -T 'change_id.short() ++ " " ++ description ++ "\n"' -r 'all()' > /home/user/repo/log_after.txt`

All six files must exist. `conflicts_after.txt` must be empty.

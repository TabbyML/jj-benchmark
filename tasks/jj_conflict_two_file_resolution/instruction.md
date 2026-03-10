You are a developer working in a jj repository at `/home/user/repo`. A rebase has created conflicts in two separate files: `server.cfg` and `client.cfg`.

Starting state:
- `base` bookmark: commit `base: add configs` with `server.cfg` containing `host=localhost` and `client.cfg` containing `port=8080`
- `main` bookmark: commit `main: update configs` with `server.cfg` containing `host=prod.server.com` and `client.cfg` containing `port=443`
- `feature` bookmark: commit `feat: feature configs` (branched from base) with `server.cfg` containing `host=dev.server.com` and `client.cfg` containing `port=9090`
- `feature` has been rebased onto `main`, creating conflicts in both files

Your tasks:

1. List conflicted files with `jj resolve --list` and save output to `/home/user/repo/conflicts_before.txt`
2. Resolve `server.cfg` by writing: `host=prod.server.com\ndebug=true\n`
3. Resolve `client.cfg` by writing: `port=443\ntimeout=30\n`
4. Verify no conflicts with `jj resolve --list` and save to `/home/user/repo/conflicts_after.txt`
5. Update the commit description: `jj describe -m "feat: feature configs (resolved)"`

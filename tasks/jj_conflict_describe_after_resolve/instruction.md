You are a developer working in a jj repository at `/home/user/repo`. After resolving a conflict in `README.md`, you need to properly describe the resolution commit with a detailed message.

Starting state:
- `base` bookmark: commit `docs: add readme` with `README.md` containing `# Project\nVersion: 1`
- `main` bookmark: commit `docs: update to v2` with `README.md` containing `# Project\nVersion: 2`
- `feature` bookmark: commit `docs: update to v3` (branched from base) with `README.md` containing `# Project\nVersion: 3`
- `feature` has been rebased onto `main`, creating a conflict in `README.md`

Your tasks:

1. Resolve the conflict in `README.md` by writing:
```
# Project
Version: 3
Changelog: merged from v2 branch
```
2. Update the commit description with a multi-line message using:
```
jj describe -m "docs: resolve version conflict

Merged version from main (v2) with feature branch (v3).
Final version set to 3 with changelog entry."
```
3. Save the commit details: `jj show --no-patch -r feature > /home/user/repo/commit_details.txt`
4. Save the full log: `jj log --no-graph -T 'description ++ "\n"' -r 'all()' > /home/user/repo/full_log.txt`
5. Verify clean: `jj resolve --list > /home/user/repo/verify_clean.txt`

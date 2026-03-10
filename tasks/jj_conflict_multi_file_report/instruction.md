You are a developer working in a jj repository at `/home/user/repo`. Multiple files have conflicts after a rebase. You need to generate a detailed report of the conflict state and then resolve all conflicts.

Starting state:
- `base` bookmark: commit `base: add project files` with three files: `api.py` (`API_VERSION=1`), `db.py` (`DB_VERSION=1`), and `ui.py` (`UI_VERSION=1`)
- `main` bookmark: commit `main: bump all versions` with `api.py` (`API_VERSION=2`), `db.py` (`DB_VERSION=2`), `ui.py` (`UI_VERSION=2`)
- `feature` bookmark: commit `feat: feature versions` (from base) with `api.py` (`API_VERSION=3`), `db.py` (`DB_VERSION=3`), `ui.py` (`UI_VERSION=3`)
- `feature` has been rebased onto `main`, creating conflicts in all three files

Your tasks:

1. Generate a conflict report:
   - `jj resolve --list > /home/user/repo/conflict_report.txt`
   - Count conflicts: `jj resolve --list | wc -l > /home/user/repo/conflict_count.txt`
2. Resolve each file:
   - `api.py`: write `API_VERSION=3\nAPI_COMPAT=2\n`
   - `db.py`: write `DB_VERSION=3\nDB_COMPAT=2\n`
   - `ui.py`: write `UI_VERSION=3\nUI_COMPAT=2\n`
3. Update description: `jj describe -m "feat: feature versions (all resolved)"`
4. Generate post-resolution report:
   - `jj resolve --list > /home/user/repo/post_report.txt`
   - `jj log --no-graph -T 'description ++ "\n"' -r 'all()' > /home/user/repo/final_log.txt`

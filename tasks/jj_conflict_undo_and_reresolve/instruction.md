You are a developer working in a jj repository at `/home/user/repo`. A conflict exists in `config.py`. You will make an incorrect resolution, undo it, and then resolve correctly.

Starting state:
- `base` bookmark: commit `base: add config` with `config.py` containing `TIMEOUT = 10`
- `main` bookmark: commit `main: increase timeout` with `config.py` containing `TIMEOUT = 60`
- `feature` bookmark: commit `feat: custom timeout` (branched from base) with `config.py` containing `TIMEOUT = 30`
- `feature` has been rebased onto `main`, creating a conflict in `config.py`

Your tasks:

1. Make a **wrong** resolution first: edit `config.py` to contain `TIMEOUT = 0` (incorrect value)
2. Undo this bad resolution using `jj op undo` to restore the conflict state
3. Verify the conflict is back with `jj resolve --list` and save output to `/home/user/repo/re_conflict.txt`
4. Now resolve correctly: edit `config.py` to contain `TIMEOUT = 60\nRETRY = 3\n`
5. Update the commit description: `jj describe -m "feat: custom timeout (resolved)"`
6. Save the final state: `jj status > /home/user/repo/final_status.txt`

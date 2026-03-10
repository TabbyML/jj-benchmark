You are a developer working in a jj repository at `/home/user/repo`. A conflicted commit is too complex to resolve. Instead, you decide to abandon it and recreate the changes cleanly on top of main.

Starting state:
- `base` bookmark: commit `base: init` with `build.sh` containing `#!/bin/bash\nBUILD=1`
- `main` bookmark: commit `main: update build` with `build.sh` containing `#!/bin/bash\nBUILD=10\nOPT=fast`
- `feature` bookmark: commit `feat: custom build` (from base) with `build.sh` containing `#!/bin/bash\nBUILD=99\nCUSTOM=true`
- `feature` has been rebased onto `main`, creating a conflict in `build.sh`

Your tasks:

1. Document the conflict before abandoning: `jj resolve --list > /home/user/repo/before_abandon.txt`
2. Abandon the conflicted `feature` commit: `jj abandon feature`
3. Verify the commit is gone: `jj log --no-graph -T 'description ++ "\n"' -r 'all()' > /home/user/repo/after_abandon_log.txt`
4. Create a new clean commit on top of `main`:
   - `jj new main`
   - Write `build.sh` with content: `#!/bin/bash\nBUILD=10\nOPT=fast\nCUSTOM=true\n`
   - `jj describe -m "feat: custom build (clean)"`
5. Save the final state:
   - `jj resolve --list > /home/user/repo/final_conflicts.txt`
   - `jj log --no-graph -T 'description ++ "\n"' -r 'all()' > /home/user/repo/final_log.txt`

The `final_conflicts.txt` must be empty. The `build.sh` must contain all required values.

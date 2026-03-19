The repository at `/home/user/repo` has a merge commit `merge-ab` that merges two branches (`branch-a` and `branch-b`) which both modified `src/config.py` from a common base. The merge has conflicts.

Resolve all conflicts in `src/config.py` keeping the database settings (host, port, name, max connections) from `branch-a` and the logging/timeout settings (LOG_LEVEL, TIMEOUT) from `branch-b`. Mark the resolution complete so no conflicts remain. Write a conflict resolution summary to `/home/user/resolution_summary.md`.

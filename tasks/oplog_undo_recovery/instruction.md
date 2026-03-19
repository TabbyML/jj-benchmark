# Recover Lost Work Using the Jujutsu Operation Log

You are a support engineer who made a mistake while working in a Jujutsu (jj) repository. You accidentally overwrote the description of an important commit with a wrong message, and then to make things worse, you ran `jj abandon` on a commit that you actually still needed. You need to recover the original state using jj's operation log (`jj op log`) and the undo mechanism (`jj undo`).

## Starting Environment

You are working in a jj repository located at `/home/user/project`. The repository already has the following commit history (from oldest to newest):

1. A commit with description **"add initial readme"** — contains a file `README.md`
2. A commit with description **"implement core feature"** — contains a file `core.py`
3. A commit with description **"add tests for core feature"** — contains a file `tests.py`

The working copy (`@`) is a new empty commit sitting on top of the "add tests for core feature" commit.

Sometime before you started this task, two destructive operations were performed:

- The description of the **"implement core feature"** commit was changed to `"WIP: bad description do not merge"` (a mistake).
- The **"add tests for core feature"** commit was abandoned (another mistake).

These two bad operations appear in the operation log.

## Your Task

Using **only `jj` commands**, recover the repository state to **before both mistakes happened**. Specifically:

1. **Inspect the operation log** with `jj op log` to understand what happened.
2. **Undo the two most recent operations** (the abandon and the bad describe) so that:
   - The commit with description `"implement core feature"` is restored (the correct description).
   - The commit with description `"add tests for core feature"` is restored (not abandoned).
3. After recovery, the commit log (`jj log`) should show all three original commits in the history:
   - `"add initial readme"`
   - `"implement core feature"`
   - `"add tests for core feature"`

## Commands to Use

You will need approximately 3–4 commands:

- `jj op log` — to inspect the operation history and identify the bad operations
- `jj op show <operation-id>` — (optional) to inspect what a specific operation changed
- `jj undo` — to undo the most recent operation (can be run twice to undo two operations)

**Do not use any Git commands.** Work exclusively with `jj`.

## Verification

After completing the recovery:

- Run `jj log --no-pager` and confirm that commits with descriptions `"add initial readme"`, `"implement core feature"`, and `"add tests for core feature"` all appear.
- Run `jj op log --no-pager` and confirm that undo operations appear at the top, showing that you recovered the state.

## Notes

- `jj undo` undoes the most recently applied operation each time it is run.
- The operation log is stored in `.jj/` inside the repository — do not manually edit it.
- All work should be performed inside `/home/user/project`.
- You do not need root/sudo access for any of these operations.
- The files `README.md`, `core.py`, and `tests.py` should be accessible in their respective commits after recovery.

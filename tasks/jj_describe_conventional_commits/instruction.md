# Describe Commits with Conventional Commit Messages

## Context

You are a release manager preparing a set of topic branches for an upcoming release. Your team uses **Conventional Commits** formatting for all commit descriptions so that automated changelog tools can generate accurate release notes from the git history.

The repository is a `jj` (Jujutsu) repository located at `/home/user/project`. It contains three commits on top of the root:

1. `chore: initialize project` — the initial trunk commit, contains `README.md`
2. A commit introducing `src/api.py` — currently has the empty/placeholder description `(no description set)`
3. A commit introducing `src/cli.py` — currently has the empty/placeholder description `(no description set)`

The working copy (`@`) is an empty change sitting on top of commit 3.

## Conventional Commits Format

Your team follows the [Conventional Commits](https://www.conventionalcommits.org/) specification. The basic format is:

```
<type>: <short summary>
```

Common types used by your team:
- `feat:` — a new feature
- `fix:` — a bug fix
- `chore:` — build process or tooling changes
- `docs:` — documentation changes
- `refactor:` — code refactoring

## Your Assignment

Using `jj describe`, update the commit descriptions for **both** undescribed commits to follow the Conventional Commits format. The exact required messages are:

### Commit 2 (introduces `src/api.py`)

Set the description to exactly:
```
feat: add REST API module
```

This commit introduces `src/api.py`, which adds the REST API implementation. Use `jj describe` targeting the parent of the working-copy parent (`@--`) and pass the message with `-m`:

```
jj describe @-- -m "feat: add REST API module"
```

### Commit 3 (introduces `src/cli.py`)

Set the description to exactly:
```
feat: add CLI module
```

This commit introduces `src/cli.py`, which adds the command-line interface. Use `jj describe` targeting the parent of the working copy (`@-`) and pass the message with `-m`:

```
jj describe @- -m "feat: add CLI module"
```

## Step-by-Step Instructions

1. **Identify the commits** — Run `jj log` to see the history and confirm the two commits with empty descriptions. The working copy is `@`, its parent is `@-` (the CLI commit), and its grandparent is `@--` (the API commit).

2. **Describe the API commit** — Run:
   ```
   jj describe @-- -m "feat: add REST API module"
   ```

3. **Describe the CLI commit** — Run:
   ```
   jj describe @- -m "feat: add CLI module"
   ```

4. **Verify** — Run `jj log --no-graph -r 'mutable() & ~@' -T 'description ++ "\n"'` to confirm both descriptions are set correctly.

## Starting Environment Assumptions

- Home directory: `/home/user`
- Repository path: `/home/user/project`
- `jj` is installed and available on `$PATH`
- User identity is pre-configured: `user.name = "Dev User"`, `user.email = "dev@example.com"`
- The repository contains exactly **three commits above root**: the trunk commit and two undescribed commits
- Commit 2 (grandparent of `@`) introduces `src/api.py` and currently has an empty description
- Commit 3 (parent of `@`) introduces `src/cli.py` and currently has an empty description
- The working copy (`@`) is an empty change with no file modifications
- No bookmarks exist other than those implied by the initial setup

## Important Notes

- Do **not** use `git` commands. All operations must use `jj`.
- Do **not** use `sudo`.
- You need exactly **2-3 jj commands** to complete this task.
- The descriptions must match **exactly** (case-sensitive, no trailing whitespace):
  - `feat: add REST API module`
  - `feat: add CLI module`
- Do not modify the trunk commit (`chore: initialize project`).
- Do not modify, create, or delete any files — only update the commit descriptions using `jj describe`.
- Do not squash, split, rebase, or otherwise restructure the commit history.
- The working copy must remain empty (no file changes) after you are done.

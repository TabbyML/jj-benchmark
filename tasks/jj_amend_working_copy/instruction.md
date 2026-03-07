You are a developer migrating from Git to `jj` (Jujutsu), working in a repository at `/home/user/repo`.

The repository has two commits above the root:
1. `chore: initial setup` — creates `README.md` with content `# My Project`
2. Your current working copy, described as `wip: add feature` — creates `feature.py` with content `def hello():\n    pass`

You realise the description `wip: add feature` is too vague. Amend it to `feat: implement hello function` using a single `jj` command. Do NOT create any new commits or modify any file contents.

After amending, save the output of `jj log --no-graph -r @ -T 'description'` to `/home/user/repo/desc.log`.

Your task is complete when:
- The working copy commit description is exactly `feat: implement hello function`
- `feature.py` is unchanged
- `/home/user/repo/desc.log` contains `feat: implement hello function`

You are a developer migrating from Git to Jujutsu (jj). You have a repository at `/home/user/project` with some tracked files that should actually be ignored.
In jj, untracking a file that is already tracked and adding it to `.gitignore` requires specific steps.

Your task:
1. Navigate to `/home/user/project`.
2. Untrack the files `app.log` and `config.local.json` from the repository, but keep them on the filesystem.
3. Create a `.gitignore` file in the root of the repository and add `*.log` and `*.local.json` to it.
4. Describe the current working copy revision with the message "chore: ignore log and local config files".
5. Create a new bookmark named `ignore-cleanup` pointing to this revision.
6. Output the commit ID of the `ignore-cleanup` bookmark to `/home/user/project/bookmark_commit.txt`.

Ensure that the working copy is correctly ignoring the files and that they are not tracked in the current revision.

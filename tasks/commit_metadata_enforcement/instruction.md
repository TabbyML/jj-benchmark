You are a repo maintainer enforcing a commit metadata policy. You have a repository at `/home/user/repo` which is already initialized with `jj`. Your task is to:
1. Configure `jj` locally in this repository to use a custom template for `jj log` by default. The template should output only the commit's short ID, the author's email, and the first line of the description, separated by ` | ` (e.g., `abc1234 | user@example.com | Fix bug`).
2. Create a new commit with the description "Update metadata policy" and ensure it is the current working copy.
3. Run `jj log -r @` and save the output to `/home/user/log_output.txt`.

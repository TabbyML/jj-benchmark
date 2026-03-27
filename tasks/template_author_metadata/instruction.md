You are a repo maintainer enforcing a metadata policy for your team's monorepo. You need to extract a custom-formatted log of the recent commits in the repository located at `/home/user/repo`.

Your task is to:
1. Navigate to `/home/user/repo`.
2. Configure a repository-specific alias named `mylog` that runs `log` with a custom template. The template must output each commit's short ID (exactly 8 characters), author name, and the first line of the commit description, separated by a pipe character `|`, followed by a newline.
3. Run your new `jj mylog` alias and redirect the output to a file named `/home/user/repo/formatted_log.txt`.

Note: Do not use `sudo` or modify system-level configurations. Ensure the alias is saved in the repository's `.jj/repo/config.toml`.

# Customize jj log output with Templates

## Background
Jujutsu (`jj`) provides a powerful functional templating language to customize the output of commands like `jj log`. You can define template aliases and use them to change the default output of `jj log`.

## Requirements
1. Initialize a new `jj` repository in the existing directory `/home/user/myproject`.
2. Create an initial commit with description "Initial commit".
3. Create a new commit with the description "Second commit".
4. Configure the repository-level `jj` config (`/home/user/myproject/.jj/repo/config.toml`) to define a custom template alias named `'custom_log'` under `[template-aliases]`.
   The alias should format a commit as: `<short_commit_id> | <author_email_local_part> | <first_line_of_description>\n`
   (e.g., `12345678 | test | Initial commit\n`).
   *Hint: Use `commit_id.short()`, `author.email().local()`, and `description.first_line()` functions.*
5. Configure the default log template in the same config file to use your `custom_log` alias (under `[templates]` set `log = 'custom_log'`).

## Implementation Guide
1. `cd` into `/home/user/myproject`.
2. Run `jj git init` to initialize the repository.
3. Set your user name to "Test User" and email to "test@example.com" in the repository config (`jj config set --repo user.name "Test User"` and `jj config set --repo user.email "test@example.com"`).
4. Use `jj describe -m "Initial commit"` to set the first commit's description.
5. Use `jj new -m "Second commit"` to create the second commit.
6. Edit `.jj/repo/config.toml` (or use `jj config set --repo`) to add the `custom_log` template alias and set it as the default `log` template.

## Constraints
- Project path: `/home/user/myproject`
- The repository must be initialized with `jj git init`.
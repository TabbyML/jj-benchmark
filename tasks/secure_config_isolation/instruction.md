You are a repo maintainer enforcing secure configuration for your team's jj repository.
You need to isolate the repository's configuration so that it overrides the global configuration with specific security settings.

Specifically, you must:
1. Initialize a new jj repository in `/home/user/secure_repo`.
2. Configure the repository-level config (`.jj/repo/config.toml`) to enforce signing by setting `signing.behavior = "own"` and `signing.backend = "gpg"`.
3. Set the repository-level user name to "Security Admin" and email to "admin@security.local".
4. Create a new commit with an empty file named `audit.log` and verify that `jj log` shows the commit successfully.

Please complete these steps using only `jj` commands where possible.


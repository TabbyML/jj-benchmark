# Ignore and Untrack a File in Jujutsu

## Background
In Jujutsu (`jj`), files in the working copy are automatically tracked. If you create a file that should be ignored (like a build artifact or log file) and it gets tracked, simply adding it to `.gitignore` is not enough to remove it from the working-copy commit. You must also explicitly untrack it.

## Requirements
You have a Jujutsu repository at `/home/user/project`. It contains a file named `build.log` which is currently tracked by `jj`.

Your task is to:
1. Add `build.log` to the `.gitignore` file in the repository root so it is ignored.
2. Untrack `build.log` in Jujutsu so it is no longer tracked by the version control system.

## Constraints
- Project path: `/home/user/project`
- **Do not delete** the `build.log` file from the filesystem. It must remain in the `/home/user/project` directory.
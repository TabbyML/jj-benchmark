# Revset Querying in Jujutsu

## Background
You are working in a Jujutsu (`jj`) repository. Jujutsu has a powerful revset language for querying revisions. Your task is to perform a series of operations to create some history, and then use a revset query to filter specific commits.

## Requirements
1. Set your `jj` configuration: user name to `Bob` and email to `bob@example.com`.
2. In the repository at `/home/user/repo`, create a new bookmark named `bob-feature` on the current working copy.
3. Create a new file `bob.txt` with the content `bob's work`.
4. Describe the current working copy (commit) with the message `Bob's first commit`.
5. Create a new commit on top of it (e.g., using `jj new`), add `more work` to `bob.txt`, and describe this new commit with `Bob's second commit`.
6. Use a `jj` revset query to find all commits authored by `Bob` that are not reachable from the `main` bookmark but are ancestors of the current working copy `@`.
7. Save the **Change IDs** (not commit IDs) of these commits into a file named `bob_commits.txt` in the root of the repository (`/home/user/repo/bob_commits.txt`), one ID per line.

## Constraints
- Project path: `/home/user/repo`
- The repository already has a `main` bookmark.
- You must use `jj` commands to complete the task.
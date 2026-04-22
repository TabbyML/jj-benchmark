# Split a Commit in Jujutsu

## Background
`jj split` can take a single commit with changes in multiple files and turn it into two separate commits.

## Requirements
- You have a repository in `/home/user/project` with a commit (described as `Combined changes`) that modifies `fileA.txt` and `fileB.txt`.
- Split this commit into two sequential commits.
- The first commit should contain only the changes to `fileA.txt` and have the description `Modify fileA`.
- The second commit should contain only the changes to `fileB.txt` and have the description `Modify fileB`.

## Implementation
1. Go to `/home/user/project`.
2. Find the revision of the `Combined changes` commit.
3. Run `jj split <revision>`.
4. Interactively (or non-interactively) place `fileA.txt` in the first commit, and `fileB.txt` in the second commit.
5. Update their descriptions using `jj describe`.

## Constraints
- Project path: `/home/user/project`.
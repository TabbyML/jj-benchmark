# Restore File from Specific Revision

## Background
You are working in a Jujutsu (`jj`) repository at `/home/user/repo`. The file `config.txt` has been modified multiple times across several commits. You need to restore `config.txt` to the exact state it was in the parent commit of the current working copy.

## Requirements
- Restore the contents of `/home/user/repo/config.txt` to match its contents in the parent revision (`@-`).
- Do not create a new commit or change the parent commit; just update the working copy of the file.

## Implementation Guide
1. Change directory to `/home/user/repo`.
2. Use `jj` commands (e.g., `jj restore -c @- config.txt` or `jj cat -r @- config.txt > config.txt`) to overwrite the current `config.txt` with its parent's version.

## Constraints
- Project path: `/home/user/repo`
- The repository must remain a valid `jj` repository.
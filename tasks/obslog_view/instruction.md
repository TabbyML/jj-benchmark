# View Change Evolution with jj obslog

## Background
In Jujutsu (`jj`), a change can evolve over time as it is amended, rebased, or otherwise updated. The `jj obslog` (or `jj evolog`) command shows the history of how a specific change has evolved, listing the previous commits that the change pointed to.

## Requirements
- Navigate to the repository at `/home/user/repo`.
- Run the `jj obslog` (or `jj evolog`) command on the current working copy commit.
- Save the full output of the command to `/home/user/obslog.txt`.

## Constraints
- Project path: `/home/user/repo`
- Output file: `/home/user/obslog.txt`
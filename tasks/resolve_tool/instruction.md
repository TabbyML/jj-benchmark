# Resolve Conflicts with Built-in Tools

## Background
Jujutsu (`jj`) supports resolving conflicts using external merge tools or built-in tools. The built-in merge tools `:ours` and `:theirs` can be used to choose side #1 and side #2 of the conflict respectively.

## Requirements
- Resolve the conflict in `file1.txt` by choosing side #1 (`:ours`).
- Resolve the conflict in `file2.txt` by choosing side #2 (`:theirs`).

## Constraints
- Project path: `/home/user/myproject`
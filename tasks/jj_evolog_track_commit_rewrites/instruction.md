You have a jj repository at `/home/user/project`. The repository contains a commit with the description `feat: add authentication module`. This commit has been through several rewrites: it was first amended to add more files, then squashed with another commit.

Your task is to use `jj evolog` (evolution log) to inspect the full rewrite history of the current working-copy commit (which has description `feat: add authentication module`). The evolog shows how a change evolved through operations.

Complete the following steps:

1. Run `jj evolog` on the current working-copy commit (`@`) to see its evolution history.
2. The evolog output shows each predecessor revision. Count the total number of entries (lines showing change IDs) in the evolog output — this includes the current revision plus all its predecessors.
3. Write a report file at `/home/user/project/evolog_report.txt` with the following exact format:

```
change_id: <the change ID of the current working-copy commit, short form — first 8 chars>
predecessor_count: <number of predecessor entries, NOT counting the current revision itself>
total_evolog_entries: <total lines in evolog including current>
```

The change ID short form is the first 8 characters of the change ID as shown by `jj log`.

For example, if the current commit has change ID `qpvuntsm...` and the evolog shows 3 entries total (current + 2 predecessors), the file should contain:
```
change_id: qpvuntsm
predecessor_count: 2
total_evolog_entries: 3
```

Do not include blank lines or extra whitespace in the report file. The file must have exactly 3 lines.

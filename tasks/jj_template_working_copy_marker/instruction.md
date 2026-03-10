You have a jj repository at `/home/user/wc-marker-repo` with several commits. Your task is to create a template that marks the working copy commit differently from regular commits in the log output.

In jj, the working copy commit is the one pointed to by `@`. You can identify it in templates using the `current_working_copy` boolean variable.

Complete the following steps:

1. Run `jj log` in `/home/user/wc-marker-repo` with:
   - `--no-graph` flag
   - `-r all()` to include all commits
   - A template that uses `current_working_copy` to mark the working copy:
     `if(current_working_copy, "[WC] ", "[  ] ") ++ description.first_line() ++ "\n"`
2. Redirect the output to `/home/user/wc-marker-repo/wc_marker_report.txt`

The output file must:
- Exist and be non-empty
- Contain at least one line starting with `[WC]` (the working copy commit)
- Contain at least one line starting with `[  ]` (regular commits)
- All non-empty lines start with either `[WC]` or `[  ]`

Example command:
```bash
jj log --no-graph -r 'all()' -T 'if(current_working_copy, "[WC] ", "[  ] ") ++ description.first_line() ++ "\n"' > /home/user/wc-marker-repo/wc_marker_report.txt
```

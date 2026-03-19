#!/bin/bash
cd /home/user/repo
jj config set --repo templates.log 'commit_id.short() ++ " | " ++ author.email() ++ " | " ++ description.first_line() ++ "\n"'
jj new -m "Update metadata policy"
jj log -r @ > /home/user/log_output.txt

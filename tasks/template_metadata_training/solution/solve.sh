#!/bin/bash
set -e

cd /home/user/repo
jj metaedit --author "Trainer <trainer@example.com>"
jj config set --user template-aliases.training_log '"commit_id.short() ++ \" - \" ++ author.email() ++ \" - \" ++ description.first_line() ++ \"\\n\""'
jj log -r "@ | @-" -T training_log --no-graph > /home/user/repo/formatted_log.txt

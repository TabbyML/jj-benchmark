#!/bin/bash
cd /home/user/repo
jj git fetch
jj rebase -r "description('My local commit')" -d "description('Coworker commit')"
jj bookmark set feature-login -r "description('My local commit')"
jj git push --bookmark feature-login

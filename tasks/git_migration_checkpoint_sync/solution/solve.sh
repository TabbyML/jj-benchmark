#!/bin/bash

# Use this file to solve the task.
cd /home/user/my-project

# 1. Create a new jj bookmark called `jj-feature-y` pointing to the same commit as `feature-x`.
jj bookmark create jj-feature-y -r feature-x

# 2. Make a new commit on `jj-feature-y` by creating a file `new_feature.txt` with the content `Hello jj` and recording the change with the description `Add new feature`.
jj new jj-feature-y
echo "Hello jj" > new_feature.txt
jj describe -m "Add new feature"
jj bookmark set jj-feature-y -r @

# 3. Export the jj bookmarks to the underlying Git repository so that Git can see the new branch `jj-feature-y`.
jj git export

# 4. Verify the export by running `git branch` and redirecting the output to a file named `git_branches.log` in the repository root.
git branch > git_branches.log

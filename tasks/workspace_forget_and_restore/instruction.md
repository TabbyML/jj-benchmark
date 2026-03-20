You are a developer working on a multi-workspace project. You need to create a new workspace to work on a feature, make a commit, and then clean up by forgetting the workspace.

Your tasks are:
1. Create a new jj workspace named `feature-workspace` at `../feature-workspace` relative to the current repository.
2. In the new workspace, create a file named `feature.txt` with the content `new feature`.
3. Create a new commit in the `feature-workspace` with the description `Add feature`.
4. Return to the original repository directory.
5. Forget the `feature-workspace` workspace using `jj workspace forget`.

Note: The original repository is located at `/home/user/repo`. The new workspace should be created at `/home/user/feature-workspace`.

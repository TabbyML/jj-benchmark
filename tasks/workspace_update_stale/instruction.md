# Update Stale Workspace

## Background
You are working in a `jj` repository at `/home/user/myproject`. Another user (or process) recently modified the repository from another workspace (`/home/user/workspace_b`), which caused your current workspace's working copy to become stale. A stale working copy means the `jj` operation log has advanced, but your working copy files haven't been updated to match the new state.

## Requirements
1. Update the stale working copy in `/home/user/myproject` so that it is no longer stale.
2. After updating, you will see that `config.json` has been modified by the other workspace (the `status` field is now `"pending"` and `new` is `true`).
3. Modify `config.json` by changing the `"status"` field from `"pending"` to `"active"`.
4. Commit the change with the exact description `"Activate config"`.

## Implementation
- Project path: `/home/user/myproject`
- Use `jj workspace update-stale` to update the stale workspace.
- Use standard text editing tools to modify `config.json`.
- Use `jj commit -m "Activate config"` to commit the change.
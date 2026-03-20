You are a repo maintainer. You need to perform a forensic analysis on the repository at `/home/user/repo` to find exactly when the `develop` branch diverged from `main`, and document your findings.

## Repository Background

The repository has two bookmarks:
- `main` — with several commits representing production releases
- `develop` — with several commits representing development work

At some point in the past, `develop` was branched off from `main`. Both branches have continued independently since then.

## Your Task

1. **Find the common ancestor** (the divergence point) using:
   ```
   jj log -r 'heads(::develop & ::main)'
   ```
   This revset finds commits that are ancestors of BOTH `develop` and `main`, then takes the heads (latest common ancestors). Note the commit description and change ID.

2. **Use `jj op log`** to find the operation where `develop` diverged from `main`:
   - Look for the operation that created the `develop` bookmark or the first commit that appears only on `develop`
   - Use `jj op log --no-graph -T 'id.short() ++ " " ++ description ++ "\n"'`

3. **Use `jj op show <OP_ID>`** on the divergence operation to confirm what changed.

4. **Identify**:
   - The commit description of the common ancestor
   - The change ID (short) of the common ancestor
   - The operation ID where divergence first occurred
   - The description of the first commit unique to `develop` (not on `main`)
   - The description of the first commit unique to `main` (not on `develop`) after the split

5. **Create `/home/user/divergence-report.md`** with this exact content:
   ```
   # Branch Divergence Report

   ## Common Ancestor
   commit_description: <DESCRIPTION>
   change_id_short: <SHORT_CHANGE_ID>

   ## Divergence Operation
   divergence_op_id: <OP_ID>

   ## First Unique Commits After Split
   first_develop_only_commit: <DESCRIPTION>
   first_main_only_commit: <DESCRIPTION>
   ```

6. **Write `/home/user/divergence_analysis_log.txt`** with:
   ```
   methodology: used heads(::develop & ::main) revset to find LCA
   common_ancestor_found: true
   divergence_op_identified: true
   report_written: /home/user/divergence-report.md
   ```

## Constraints

- Working directory: `/home/user/repo`
- Use `jj` commands for all analysis
- Both output files must be created with the exact formats shown

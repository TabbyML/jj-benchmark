import os
import subprocess
import pytest

REPO_DIR = "/home/user/project"


def test_auth_module_commit_visible():
    # The "add user authentication module" commit must exist and be visible (not abandoned)
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description",
         "-r", 'description(substring:"add user authentication module")'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"jj log failed when querying for 'add user authentication module': {result.stderr}"
    )
    assert "add user authentication module" in result.stdout, (
        "The 'add user authentication module' commit is not visible in the revision log. "
        "It may still be abandoned. Use 'jj op log' and 'jj undo' or 'jj op restore' to recover it."
    )


def test_src_auth_py_content_in_auth_commit():
    # src/auth.py must exist with correct content in the auth module commit
    result = subprocess.run(
        ["jj", "file", "show",
         "-r", 'description(substring:"add user authentication module")',
         "src/auth.py"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"src/auth.py not found in 'add user authentication module' commit: {result.stderr}"
    )
    assert "# Authentication module" in result.stdout, (
        f"src/auth.py in 'add user authentication module' does not contain '# Authentication module'. "
        f"Got: {result.stdout!r}"
    )


def test_update_readme_parent_is_auth_module():
    # The "update README with usage instructions" commit must have
    # "add user authentication module" as its parent
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description",
         "-r", 'parents(description(substring:"update README with usage instructions"))'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Failed to query parents of 'update README with usage instructions': {result.stderr}"
    )
    assert "add user authentication module" in result.stdout, (
        "The parent of 'update README with usage instructions' is not 'add user authentication module'. "
        f"Got parents: {result.stdout!r}. The ancestry chain was not fully restored."
    )


def test_auth_module_parent_is_initial_scaffold():
    # The "add user authentication module" commit must have
    # "initial project scaffold" as its parent
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description",
         "-r", 'parents(description(substring:"add user authentication module"))'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Failed to query parents of 'add user authentication module': {result.stderr}"
    )
    assert "initial project scaffold" in result.stdout, (
        "The parent of 'add user authentication module' is not 'initial project scaffold'. "
        f"Got parents: {result.stdout!r}. The ancestry chain was not fully restored."
    )


def test_main_bookmark_points_to_update_readme():
    # The 'main' bookmark must point to the "update README with usage instructions" commit
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description",
         "-r", "main"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Failed to resolve 'main' bookmark: {result.stderr}"
    )
    assert "update README with usage instructions" in result.stdout, (
        "The 'main' bookmark does not point to 'update README with usage instructions'. "
        f"Got: {result.stdout!r}"
    )


def test_working_copy_is_empty_on_top_of_main():
    # The working copy (@) must be an empty change on top of the 'main' bookmark commit
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description",
         "-r", "parents(@)"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"Failed to query parent of working copy: {result.stderr}"
    )
    assert "update README with usage instructions" in result.stdout, (
        "The working-copy commit (@) parent is not 'update README with usage instructions'. "
        f"Got: {result.stdout!r}"
    )

    # Verify working copy is empty
    result_status = subprocess.run(
        ["jj", "diff", "--summary"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result_status.returncode == 0, (
        f"jj diff --summary failed: {result_status.stderr}"
    )
    assert result_status.stdout.strip() == "", (
        f"Working copy is not empty. It has pending changes: {result_status.stdout!r}"
    )


def test_operation_log_has_undo_or_restore():
    # The operation log must contain an undo/restore/revert operation,
    # confirming the recovery was performed via the operation log.
    result = subprocess.run(
        ["jj", "op", "log", "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    op_log = result.stdout.lower()
    has_undo = "undo" in op_log
    has_restore = "restore" in op_log
    has_revert = "revert" in op_log
    assert has_undo or has_restore or has_revert, (
        "No undo, restore, or revert operation found in the operation log. "
        "The recovery must be performed via the jj operation log (jj undo or jj op restore), "
        f"not by manually recreating the commit. Op log: {result.stdout!r}"
    )

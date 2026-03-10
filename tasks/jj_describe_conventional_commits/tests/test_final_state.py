import os
import subprocess
import pytest

REPO_DIR = "/home/user/project"


def run(cmd, cwd=REPO_DIR):
    env = dict(os.environ)
    env["JJ_NO_PAGER"] = "1"
    env["PAGER"] = "cat"
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd, env=env
    )
    return result


def test_api_commit_has_correct_description():
    """The commit that introduces src/api.py now has the description 'feat: add REST API module'."""
    result = run(
        "jj log --no-graph -r 'description(exact:\"feat: add REST API module\\n\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add REST API module" in result.stdout, (
        f"Expected commit with description 'feat: add REST API module'. Got: {result.stdout!r}"
    )


def test_cli_commit_has_correct_description():
    """The commit that introduces src/cli.py now has the description 'feat: add CLI module'."""
    result = run(
        "jj log --no-graph -r 'description(exact:\"feat: add CLI module\\n\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add CLI module" in result.stdout, (
        f"Expected commit with description 'feat: add CLI module'. Got: {result.stdout!r}"
    )


def test_api_commit_contains_api_py():
    """The commit described as 'feat: add REST API module' has src/api.py in its file tree."""
    result = run(
        "jj file list -r 'description(exact:\"feat: add REST API module\\n\")'"
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "src/api.py" in result.stdout, (
        f"src/api.py not found in 'feat: add REST API module' commit. Got: {result.stdout!r}"
    )


def test_cli_commit_contains_cli_py():
    """The commit described as 'feat: add CLI module' has src/cli.py in its file tree."""
    result = run(
        "jj file list -r 'description(exact:\"feat: add CLI module\\n\")'"
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "src/cli.py" in result.stdout, (
        f"src/cli.py not found in 'feat: add CLI module' commit. Got: {result.stdout!r}"
    )


def test_trunk_commit_unchanged():
    """The trunk commit 'chore: initialize project' still exists and was not modified."""
    result = run(
        "jj log --no-graph -r 'description(exact:\"chore: initialize project\\n\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "chore: initialize project" in result.stdout, (
        f"Trunk commit 'chore: initialize project' not found. Got: {result.stdout!r}"
    )


def test_no_empty_descriptions_remain():
    """No mutable non-working-copy commits have empty descriptions."""
    result = run(
        "jj log --no-graph -r 'mutable() & ~@ & description(\"\")' "
        "-T 'change_id ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    assert len(lines) == 0, (
        f"Expected 0 commits with empty descriptions, but found {len(lines)}: {result.stdout!r}"
    )


def test_working_copy_is_still_empty():
    """The working copy has not been modified."""
    result = run("jj diff -r @")
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Working copy should still be empty. Diff: {result.stdout}"
    )


def test_commit_structure_intact():
    """Exactly 3 mutable commits exist (api commit, cli commit, empty working copy)."""
    result = run(
        "jj log --no-graph -r 'mutable()' "
        "-T 'change_id ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    assert len(lines) == 3, (
        f"Expected exactly 3 mutable commits, got {len(lines)}: {result.stdout!r}"
    )

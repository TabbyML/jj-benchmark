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


def test_jj_binary_exists():
    result = run("which jj", cwd="/tmp")
    assert result.returncode == 0, "jj binary not found on PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repo directory {REPO_DIR} does not exist"


def test_repo_jj_directory_exists():
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj")), (
        f".jj directory not found in {REPO_DIR}"
    )


def test_repo_is_valid_jj_repo():
    result = run("jj root")
    assert result.returncode == 0, f"Not a valid jj repo: {result.stderr}"


def test_jj_status_succeeds():
    result = run("jj status")
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_readme_exists():
    assert os.path.isfile(os.path.join(REPO_DIR, "README.md")), (
        "README.md not found in project repo"
    )


def test_src_api_py_exists():
    assert os.path.isfile(os.path.join(REPO_DIR, "src", "api.py")), (
        "src/api.py not found in project repo"
    )


def test_src_cli_py_exists():
    assert os.path.isfile(os.path.join(REPO_DIR, "src", "cli.py")), (
        "src/cli.py not found in project repo"
    )


def test_trunk_commit_exists():
    """Commit with 'chore: initialize project' description exists."""
    result = run(
        "jj log --no-graph -r 'description(substring:\"chore: initialize project\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "chore: initialize project" in result.stdout, (
        f"Trunk commit not found. Got: {result.stdout!r}"
    )


def test_src_api_py_in_grandparent_commit():
    """The grandparent commit (@--) contains src/api.py in its file tree."""
    result = run("jj file list -r '@--'")
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "src/api.py" in result.stdout, (
        f"src/api.py not found in @--. Got: {result.stdout!r}"
    )


def test_src_cli_py_in_parent_commit():
    """The parent commit (@-) contains src/cli.py in its file tree."""
    result = run("jj file list -r '@-'")
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "src/cli.py" in result.stdout, (
        f"src/cli.py not found in @-. Got: {result.stdout!r}"
    )


def test_two_undescribed_mutable_commits_exist():
    """Exactly two mutable non-working-copy commits exist with empty descriptions."""
    result = run(
        "jj log --no-graph -r 'mutable() & ~@ & description(\"\")' "
        "-T 'change_id ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    assert len(lines) == 2, (
        f"Expected exactly 2 commits with empty descriptions, got {len(lines)}: {result.stdout!r}"
    )


def test_working_copy_is_empty():
    """The working copy commit has no file changes."""
    result = run("jj diff -r @")
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Working copy is not empty. Diff: {result.stdout}"
    )


def test_api_commit_description_is_empty():
    """The grandparent commit (@--) currently has an empty description."""
    result = run("jj log --no-graph -r '@--' -T 'description'")
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"@-- should have empty description, got: {result.stdout!r}"
    )


def test_cli_commit_description_is_empty():
    """The parent commit (@-) currently has an empty description."""
    result = run("jj log --no-graph -r '@-' -T 'description'")
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"@- should have empty description, got: {result.stdout!r}"
    )

import os
import subprocess
import pytest

REPO = "/home/user/repo"


def jj(*args, **kwargs):
    env = os.environ.copy()
    env["HOME"] = "/home/user"
    return subprocess.run(
        ["jj"] + list(args),
        cwd=REPO,
        capture_output=True,
        text=True,
        env=env,
        **kwargs
    )


def test_repo_exists():
    assert os.path.isdir(REPO), "Repo directory should exist"
    assert os.path.isdir(os.path.join(REPO, ".jj")), ".jj directory should exist"


def test_bookmarks_exist():
    result = jj("bookmark", "list")
    assert result.returncode == 0
    output = result.stdout
    assert "base" in output, "bookmark 'base' should exist"
    assert "branch-a" in output, "bookmark 'branch-a' should exist"
    assert "branch-b" in output, "bookmark 'branch-b' should exist"
    assert "merge-ab" in output, "bookmark 'merge-ab' should exist"


def test_merge_commit_has_two_parents():
    # Check by counting parent commits using revsets
    result = jj("log", "-r", "parents(merge-ab)", "--no-graph", "-T", 'description ++ "\n"')
    assert result.returncode == 0
    lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 2, f"merge-ab should have 2 parents, got: {result.stdout}"


def test_conflict_exists_in_merge():
    result = jj("resolve", "--list", "-r", "merge-ab")
    assert result.returncode == 0
    assert "src/config.py" in result.stdout, "src/config.py should have conflicts in merge-ab"


def test_config_file_exists_at_base():
    result = jj("file", "show", "src/config.py", "-r", "base")
    assert result.returncode == 0
    assert "DATABASE_HOST" in result.stdout
    assert "LOG_LEVEL" in result.stdout


def test_branch_a_changes():
    result = jj("file", "show", "src/config.py", "-r", "branch-a")
    assert result.returncode == 0
    assert "db.production.example.com" in result.stdout
    assert "5433" in result.stdout
    assert "mydb_prod" in result.stdout
    assert "50" in result.stdout


def test_branch_b_changes():
    result = jj("file", "show", "src/config.py", "-r", "branch-b")
    assert result.returncode == 0
    assert "DEBUG" in result.stdout
    assert "60" in result.stdout

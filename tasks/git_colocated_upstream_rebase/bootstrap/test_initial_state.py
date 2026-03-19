import os
import subprocess
import pytest


REPO = "/home/user/local-repo"


def run_jj(args, cwd=REPO):
    return subprocess.run(
        ["jj"] + args,
        cwd=cwd,
        capture_output=True,
        text=True
    )


def test_repo_exists():
    assert os.path.isdir(REPO)


def test_upstream_git_exists():
    assert os.path.isdir("/home/user/upstream.git")


def test_local_three_commits():
    result = run_jj(["log", "--no-graph", "-r", "mutable()",
                     "-T", 'description ++ "\n"'])
    assert result.returncode == 0
    for i in range(1, 4):
        assert f"local-{i}" in result.stdout, f"local-{i} should exist"


def test_main_bookmark_on_old_upstream():
    """main should currently point to upstream-2, not the newer upstream commits."""
    result = run_jj(["file", "show", "features.txt", "-r", "main"])
    assert result.returncode == 0
    # Should have the old version (no security= line)
    assert "security=strict" not in result.stdout, \
        "main should be on old upstream (before upstream-3)"


def test_upstream_has_new_commits():
    """The upstream remote should have newer commits not yet fetched."""
    result = subprocess.run(
        ["git", "log", "--oneline", "main"],
        cwd="/home/user/upstream.git",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "upstream-3" in result.stdout or "upstream-4" in result.stdout, \
        "upstream.git should have newer commits"


def test_local_branch_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert result.returncode == 0
    assert "local-branch" in result.stdout


def test_local_state_file_exists():
    assert os.path.isfile("/home/user/local_state.txt")

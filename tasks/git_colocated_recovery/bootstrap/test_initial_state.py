"""
Tests for jj_git_colocated_recovery task.
Verifies the INITIAL bad state of the colocated jj+git repo.
"""
import os
import subprocess

REPO_DIR = "/home/user/myrepo"


def run_jj(args, cwd=REPO_DIR):
    return subprocess.run(["jj"] + args, cwd=cwd, capture_output=True, text=True)


def run_git(args, cwd=REPO_DIR):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)


def test_repo_exists():
    assert os.path.isdir(REPO_DIR), f"Repo directory {REPO_DIR} does not exist"


def test_is_colocated():
    """Both .jj and .git should exist in the repo."""
    assert os.path.isdir(os.path.join(REPO_DIR, ".jj")), ".jj directory missing"
    assert os.path.isdir(os.path.join(REPO_DIR, ".git")), ".git directory missing"


def test_git_head_is_detached():
    """Git HEAD should be detached."""
    result = run_git(["symbolic-ref", "--quiet", "HEAD"])
    # Returns non-zero if HEAD is detached
    assert result.returncode != 0, "Git HEAD is NOT detached - expected detached state"


def test_uncommitted_changes_exist():
    """There should be uncommitted changes in the working directory."""
    assert os.path.isfile(os.path.join(REPO_DIR, "config.py")), \
        "config.py should exist as an uncommitted change"
    with open(os.path.join(REPO_DIR, "config.py")) as f:
        content = f.read()
    assert "IMPORTANT_CONFIG" in content, "config.py should contain IMPORTANT_CONFIG"


def test_main_bookmark_exists():
    """main bookmark should exist in jj."""
    result = run_jj(["bookmark", "list"])
    assert result.returncode == 0
    assert "main" in result.stdout, f"main bookmark not found: {result.stdout}"


def test_previous_commits_exist():
    """At least 3 commits should exist in jj history."""
    result = run_jj(["log", "--no-graph", "-r", "all()", "-T", 'commit_id ++ "\\n"'])
    assert result.returncode == 0
    commits = [l for l in result.stdout.strip().splitlines() if l.strip() and l.strip() != "0" * 40]
    assert len(commits) >= 3, f"Expected at least 3 commits, got {len(commits)}"


def test_no_recovery_commit_yet():
    """No commit with 'recovery' or 'preserved' in description should exist yet."""
    result = run_jj([
        "log", "--no-graph", "-r", "all()",
        "-T", 'description ++ "\\n"'
    ])
    assert result.returncode == 0
    for line in result.stdout.splitlines():
        assert "recovery" not in line.lower() or "wip" in line.lower(), \
            f"Recovery commit already exists: {line}"


def test_no_sync_report_yet():
    assert not os.path.isfile("/home/user/sync_report.txt"), \
        "sync_report.txt should not exist in initial state"

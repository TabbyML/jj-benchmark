"""
Tests for jj_git_colocated_recovery task.
Verifies the FINAL state after the user reconciles the colocated repo.
All tests here must FAIL before the task is done.
"""
import os
import subprocess

REPO_DIR = "/home/user/myrepo"


def run_jj(args, cwd=REPO_DIR):
    return subprocess.run(["jj"] + args, cwd=cwd, capture_output=True, text=True)


def run_git(args, cwd=REPO_DIR):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)


def test_git_head_not_detached():
    """Git HEAD should no longer be detached after recovery."""
    result = run_git(["symbolic-ref", "--quiet", "HEAD"])
    assert result.returncode == 0, \
        f"Git HEAD is still detached after recovery: {result.stderr}"


def test_config_py_committed():
    """config.py must be committed (not just in working dir as untracked change)."""
    # Check it exists in jj history
    result = run_jj([
        "log", "--no-graph", "-r", "all()",
        "-T", 'description ++ "\\n"'
    ])
    assert result.returncode == 0
    # Also verify config.py is committed in some commit
    result2 = run_jj(["file", "show", "-r", "main", "config.py"])
    assert result2.returncode == 0, \
        f"config.py not committed in main: {result2.stderr}"
    assert "IMPORTANT_CONFIG" in result2.stdout, \
        "IMPORTANT_CONFIG not found in committed config.py"


def test_readme_modification_preserved():
    """The README.md modification must be in the committed state."""
    result = run_jj(["file", "show", "-r", "main", "README.md"])
    assert result.returncode == 0, f"README.md not accessible: {result.stderr}"
    assert "This change must be preserved" in result.stdout, \
        "The README.md modification was not preserved in the commit"


def test_jj_and_git_in_sync():
    """jj and git must refer to the same commit for main."""
    jj_result = run_jj([
        "log", "--no-graph", "-r", "main",
        "-T", 'commit_id ++ "\\n"'
    ])
    assert jj_result.returncode == 0
    jj_hash = jj_result.stdout.strip()
    assert jj_hash, "Could not get main commit hash from jj"

    git_result = run_git(["rev-parse", "main"])
    assert git_result.returncode == 0
    git_hash = git_result.stdout.strip()
    assert git_hash, "Could not get main commit hash from git"

    assert jj_hash == git_hash, \
        f"jj main ({jj_hash}) and git main ({git_hash}) diverged"


def test_core_py_still_present():
    """Original core.py must still be in main."""
    result = run_jj(["file", "show", "-r", "main", "core.py"])
    assert result.returncode == 0, f"core.py not found in main: {result.stderr}"
    assert "def core" in result.stdout


def test_sync_report_exists():
    assert os.path.isfile("/home/user/sync_report.txt"), \
        "sync_report.txt does not exist"


def test_sync_report_content():
    with open("/home/user/sync_report.txt") as f:
        content = f.read()
    assert len(content.strip()) > 30, "sync_report.txt is too short"
    assert "jj" in content.lower() or "git" in content.lower(), \
        "sync_report.txt must mention jj or git"

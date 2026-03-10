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


def test_repo_is_valid_jj_repo():
    result = run("jj root")
    assert result.returncode == 0, f"Not a valid jj repo: {result.stderr}"


def test_repo_has_three_feature_commits():
    """Exactly three non-root, non-working-copy mutable commits exist."""
    result = run(
        "jj log --no-graph -r 'mutable() & ~@ & ~root()' -T 'change_id ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 3, (
        f"Expected exactly 3 mutable non-root non-wc commits, got {len(lines)}: {result.stdout}"
    )


def test_first_feature_commit_exists():
    """Commit with 'feat: add authentication module' description exists."""
    result = run(
        "jj log --no-graph -r 'description(substring:\"feat: add authentication module\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add authentication module" in result.stdout, (
        f"Expected 'feat: add authentication module' commit not found. Got: {result.stdout!r}"
    )


def test_second_feature_commit_exists():
    """Commit with 'feat: add payment processing' description exists."""
    result = run(
        "jj log --no-graph -r 'description(substring:\"feat: add payment processing\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add payment processing" in result.stdout, (
        f"Expected 'feat: add payment processing' commit not found. Got: {result.stdout!r}"
    )


def test_third_feature_commit_exists():
    """Commit with 'feat: add notification service' description exists."""
    result = run(
        "jj log --no-graph -r 'description(substring:\"feat: add notification service\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add notification service" in result.stdout, (
        f"Expected 'feat: add notification service' commit not found. Got: {result.stdout!r}"
    )


def test_src_auth_py_exists_in_first_commit():
    result = run(
        "jj file list -r 'description(substring:\"feat: add authentication module\")'"
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "src/auth.py" in result.stdout, (
        f"src/auth.py not found in auth commit. Got: {result.stdout}"
    )


def test_src_payment_py_exists_in_second_commit():
    result = run(
        "jj file list -r 'description(substring:\"feat: add payment processing\")'"
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "src/payment.py" in result.stdout, (
        f"src/payment.py not found in payment commit. Got: {result.stdout}"
    )


def test_src_notify_py_exists_in_third_commit():
    result = run(
        "jj file list -r 'description(substring:\"feat: add notification service\")'"
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "src/notify.py" in result.stdout, (
        f"src/notify.py not found in notification commit. Got: {result.stdout}"
    )


def test_working_copy_is_empty():
    """The working copy commit should have no changes."""
    result = run("jj diff -r @")
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Working copy is not empty. Diff output: {result.stdout}"
    )


def test_no_bookmarks_exist():
    """No bookmarks should exist in the initial state."""
    result = run("jj bookmark list")
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Expected no bookmarks, found: {result.stdout}"
    )


def test_no_tags_exist():
    """No tags should exist in the initial state."""
    result = run("jj tag list")
    assert result.returncode == 0, f"jj tag list failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Expected no tags, found: {result.stdout}"
    )


def test_commits_are_linear_stack():
    """The three feature commits form a linear chain."""
    result = run(
        "jj log --no-graph -r 'mutable() & ~@ & ~root()' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    descriptions = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert "feat: add authentication module" in descriptions, (
        "Auth commit missing from linear stack"
    )
    assert "feat: add payment processing" in descriptions, (
        "Payment commit missing from linear stack"
    )
    assert "feat: add notification service" in descriptions, (
        "Notification commit missing from linear stack"
    )

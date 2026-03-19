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


def test_feature_auth_bookmark_exists():
    """Bookmark 'feature/auth' still exists after the task."""
    result = run("jj bookmark list")
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature/auth" in result.stdout, (
        f"Bookmark 'feature/auth' not found. Got: {result.stdout!r}"
    )


def test_feature_password_reset_bookmark_exists():
    """Bookmark 'feature/password-reset' was created."""
    result = run("jj bookmark list")
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature/password-reset" in result.stdout, (
        f"Bookmark 'feature/password-reset' not found. Got: {result.stdout!r}"
    )


def test_feature_auth_points_to_password_reset_commit():
    """Bookmark 'feature/auth' now points to the 'feat: implement password reset' commit."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"feature/auth\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: implement password reset" in result.stdout, (
        f"Bookmark 'feature/auth' should point to password reset commit. Got: {result.stdout!r}"
    )


def test_feature_password_reset_points_to_password_reset_commit():
    """Bookmark 'feature/password-reset' points to the 'feat: implement password reset' commit."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"feature/password-reset\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: implement password reset" in result.stdout, (
        f"Bookmark 'feature/password-reset' should point to password reset commit. "
        f"Got: {result.stdout!r}"
    )


def test_both_bookmarks_point_to_same_commit():
    """Both bookmarks resolve to the same commit."""
    result = run(
        "jj log --no-graph "
        "-r 'bookmarks(\"feature/auth\") & bookmarks(\"feature/password-reset\")' "
        "-T 'change_id ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 1, (
        f"Expected both bookmarks to point to the same commit (1 result), "
        f"got {len(lines)}: {result.stdout!r}"
    )


def test_feature_auth_points_to_wc_parent():
    """Bookmark 'feature/auth' points to @- (the parent of the working copy)."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"feature/auth\") & @-' "
        "-T 'change_id ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 1, (
        f"Bookmark 'feature/auth' is not pointing at @-. Got: {result.stdout!r}"
    )


def test_feature_password_reset_points_to_wc_parent():
    """Bookmark 'feature/password-reset' points to @- (the parent of the working copy)."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"feature/password-reset\") & @-' "
        "-T 'change_id ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 1, (
        f"Bookmark 'feature/password-reset' is not pointing at @-. Got: {result.stdout!r}"
    )


def test_commit_history_intact():
    """The original two feature commits still exist and were not modified."""
    for desc in ["feat: implement user login", "feat: implement password reset"]:
        result = run(
            f"jj log --no-graph -r 'description(substring:\"{desc}\")' "
            "-T 'change_id ++ \"\\n\"'"
        )
        assert result.returncode == 0, f"jj log failed: {result.stderr}"
        lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
        assert len(lines) == 1, (
            f"Expected exactly 1 commit for '{desc}', got {len(lines)}: {result.stdout!r}"
        )


def test_working_copy_is_still_empty():
    """The working copy has not been modified."""
    result = run("jj diff -r @")
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Working copy should still be empty. Diff: {result.stdout}"
    )

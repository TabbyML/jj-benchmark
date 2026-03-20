import os
import subprocess
import pytest

REPO_DIR = "/home/user/webapp"


def run(cmd, cwd=REPO_DIR):
    env = dict(os.environ)
    env["JJ_NO_PAGER"] = "1"
    env["PAGER"] = "cat"
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd, env=env
    )
    return result


def test_dev_bookmark_exists():
    """Bookmark 'dev' still exists."""
    result = run("jj bookmark list")
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "dev" in result.stdout, (
        f"Bookmark 'dev' not found. Got: {result.stdout!r}"
    )


def test_dev_bookmark_points_to_contact_commit():
    """Bookmark 'dev' points to the 'feat: add contact page' commit."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"dev\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add contact page" in result.stdout, (
        f"Bookmark 'dev' should point to contact commit. Got: {result.stdout!r}"
    )


def test_feature_contact_bookmark_exists():
    """Bookmark 'feature/contact' exists."""
    result = run("jj bookmark list")
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature/contact" in result.stdout, (
        f"Bookmark 'feature/contact' not found. Got: {result.stdout!r}"
    )


def test_feature_contact_bookmark_points_to_contact_commit():
    """Bookmark 'feature/contact' points to the 'feat: add contact page' commit."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"feature/contact\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add contact page" in result.stdout, (
        f"Bookmark 'feature/contact' should point to contact commit. Got: {result.stdout!r}"
    )


def test_both_bookmarks_point_to_same_commit():
    """Both bookmarks 'dev' and 'feature/contact' point to the same revision."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"dev\") & bookmarks(\"feature/contact\")' "
        "-T 'change_id ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 1, (
        f"Expected both bookmarks on same commit (1 line), got {len(lines)}: {result.stdout!r}"
    )


def test_dev_bookmark_points_to_working_copy_parent():
    """Bookmark 'dev' points to @- (parent of working copy)."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"dev\") & @-' "
        "-T 'change_id ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) >= 1, (
        f"Bookmark 'dev' should point to @-. Got: {result.stdout!r}"
    )


def test_feature_contact_bookmark_points_to_working_copy_parent():
    """Bookmark 'feature/contact' points to @- (parent of working copy)."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"feature/contact\") & @-' "
        "-T 'change_id ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) >= 1, (
        f"Bookmark 'feature/contact' should point to @-. Got: {result.stdout!r}"
    )


def test_original_commit_structure_intact():
    """Both feature commits still exist in the history."""
    for desc in ["feat: add homepage route", "feat: add contact page"]:
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
    """The working copy has no pending changes."""
    result = run("jj diff -r @")
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Working copy should be empty. Diff: {result.stdout}"
    )

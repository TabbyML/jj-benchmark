import os
import subprocess
import pytest

REPO_DIR = "/home/user/project"
FEATURE_FILE = "/home/user/project/feature.txt"


def run_jj(*args, **kwargs):
    result = subprocess.run(
        ["jj", "--no-pager"] + list(args),
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
        **kwargs,
    )
    return result


def test_feature_bookmark_exists():
    """The 'feature' bookmark must be present after recovery."""
    result = run_jj("bookmark", "list")
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature" in result.stdout, (
        f"'feature' bookmark not found in bookmark list.\nOutput:\n{result.stdout}"
    )


def test_implement_feature_commit_exists():
    """The commit 'implement feature' must be visible in jj log."""
    result = run_jj("log", "--no-graph", "-r", 'description(substring:"implement feature")')
    assert result.returncode == 0, (
        f"jj log failed to find 'implement feature' commit.\nStderr: {result.stderr}"
    )
    assert "implement feature" in result.stdout, (
        f"'implement feature' commit not found in log output.\nOutput:\n{result.stdout}"
    )


def test_feature_bookmark_points_to_implement_feature_commit():
    """The 'feature' bookmark must point to the 'implement feature' commit."""
    # Get the description of the commit 'feature' bookmark points to
    result_bm = run_jj(
        "log", "--no-graph", "-r", "feature",
        "--template", 'description ++ "\n"'
    )
    assert result_bm.returncode == 0, (
        f"Failed to resolve 'feature' bookmark: {result_bm.stderr}"
    )
    assert "implement feature" in result_bm.stdout, (
        f"'feature' bookmark does not point to 'implement feature' commit.\n"
        f"Bookmark points to commit with description: {result_bm.stdout.strip()}"
    )


def test_feature_file_exists():
    """The file feature.txt must exist at /home/user/project/feature.txt."""
    assert os.path.isfile(FEATURE_FILE), (
        f"feature.txt does not exist at {FEATURE_FILE}"
    )


def test_feature_file_content():
    """feature.txt must contain 'feature work'."""
    assert os.path.isfile(FEATURE_FILE), f"feature.txt not found at {FEATURE_FILE}"
    with open(FEATURE_FILE, "r") as fh:
        content = fh.read()
    assert content.strip() == "feature work", (
        f"feature.txt has unexpected content: {repr(content)}"
    )


def test_op_log_has_undo_operation():
    """The operation log must contain an undo/restore operation as evidence of recovery."""
    result = run_jj("op", "log", "--no-graph", "--limit", "3")
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    output_lower = result.stdout.lower()
    # The most recent ops should include one of these recovery patterns
    assert any(keyword in output_lower for keyword in ["undo", "restore"]), (
        f"No undo or restore operation found in recent operation log.\n"
        f"Operation log:\n{result.stdout}"
    )


def test_implement_feature_commit_has_feature_file():
    """Verify feature.txt is part of the 'implement feature' commit in jj history."""
    result = run_jj(
        "file", "show", "-r", 'description(substring:"implement feature")', "feature.txt"
    )
    assert result.returncode == 0, (
        f"Failed to show feature.txt in 'implement feature' commit.\nStderr: {result.stderr}"
    )
    assert "feature work" in result.stdout, (
        f"feature.txt in the commit does not contain 'feature work'.\nOutput: {result.stdout}"
    )

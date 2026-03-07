import os
import subprocess
import pytest


REPO_DIR = "/home/user/myproject"
ORIGIN_REMOTE = "/home/user/remotes/origin.git"
UPSTREAM_REMOTE = "/home/user/remotes/upstream.git"


def test_origin_remote_still_configured():
    result = subprocess.run(
        ["jj", "git", "remote", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj git remote list failed: {result.stderr}"
    assert "origin" in result.stdout, f"'origin' remote not found after task completion"


def test_upstream_remote_still_configured():
    result = subprocess.run(
        ["jj", "git", "remote", "list"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj git remote list failed: {result.stderr}"
    assert "upstream" in result.stdout, f"'upstream' remote not found after task completion"


def test_feature_bookmark_exists_on_origin():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--all-remotes"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list --all-remotes failed: {result.stderr}"
    assert "feature@origin" in result.stdout, (
        f"'feature@origin' not found in bookmark list. Output:\n{result.stdout}"
    )


def test_feature_bookmark_exists_on_upstream():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--all-remotes"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list --all-remotes failed: {result.stderr}"
    assert "feature@upstream" in result.stdout, (
        f"'feature@upstream' not found in bookmark list. Output:\n{result.stdout}"
    )


def test_upstream_git_repo_has_feature_branch():
    result = subprocess.run(
        ["git", "-C", UPSTREAM_REMOTE, "branch", "--list", "feature"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git branch list failed: {result.stderr}"
    assert "feature" in result.stdout, (
        f"'feature' branch not found in upstream git repo: {result.stdout}"
    )


def test_upstream_feature_tip_commit_message():
    result = subprocess.run(
        ["git", "-C", UPSTREAM_REMOTE, "log", "feature", "--oneline", "-1"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git log failed: {result.stderr}"
    assert "prepare upstream submission" in result.stdout, (
        f"Latest commit on upstream feature branch does not have expected message. "
        f"Got: {result.stdout}"
    )


def test_submission_file_exists():
    submission_path = os.path.join(REPO_DIR, "SUBMISSION.md")
    assert os.path.isfile(submission_path), (
        f"SUBMISSION.md not found at {submission_path}"
    )


def test_submission_file_content():
    submission_path = os.path.join(REPO_DIR, "SUBMISSION.md")
    with open(submission_path, "r") as f:
        content = f.read()
    assert "upstream ready" in content, (
        f"SUBMISSION.md does not contain 'upstream ready'. Content: {content!r}"
    )


def test_prepare_upstream_submission_commit_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description", "-r",
         "description(substring:'prepare upstream submission')"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "prepare upstream submission" in result.stdout, (
        f"No commit with description 'prepare upstream submission' found"
    )


def test_feature_bookmark_not_behind_upstream():
    # feature bookmark should be in sync or ahead of feature@upstream
    # Check that feature@upstream exists and feature (local) is not behind it
    result = subprocess.run(
        ["jj", "bookmark", "list", "--all-remotes", "feature"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    # The output should not show a conflict marker (?) for feature
    lines = [l for l in result.stdout.splitlines() if "feature" in l and "?" in l]
    assert len(lines) == 0, f"feature bookmark appears conflicted: {result.stdout}"


def test_origin_feature_branch_exists():
    result = subprocess.run(
        ["git", "-C", ORIGIN_REMOTE, "branch", "--list", "feature"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"git branch list failed: {result.stderr}"
    assert "feature" in result.stdout, (
        f"'feature' branch not found in origin git repo: {result.stdout}"
    )

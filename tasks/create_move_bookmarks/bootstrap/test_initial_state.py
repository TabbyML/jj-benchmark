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


def test_src_login_py_exists():
    assert os.path.isfile(os.path.join(REPO_DIR, "src", "login.py")), (
        "src/login.py not found in project repo"
    )


def test_src_reset_py_exists():
    assert os.path.isfile(os.path.join(REPO_DIR, "src", "reset.py")), (
        "src/reset.py not found in project repo"
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


def test_login_commit_exists():
    """Commit with 'feat: implement user login' description exists."""
    result = run(
        "jj log --no-graph -r 'description(substring:\"feat: implement user login\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: implement user login" in result.stdout, (
        f"Login commit not found. Got: {result.stdout!r}"
    )


def test_password_reset_commit_exists():
    """Commit with 'feat: implement password reset' description exists."""
    result = run(
        "jj log --no-graph -r 'description(substring:\"feat: implement password reset\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: implement password reset" in result.stdout, (
        f"Password reset commit not found. Got: {result.stdout!r}"
    )


def test_two_mutable_feature_commits_exist():
    """Exactly two feature commits exist (login and password reset)."""
    for desc in ["feat: implement user login", "feat: implement password reset"]:
        result = run(
            f"jj log --no-graph -r 'description(substring:\"{desc}\")' "
            "-T 'change_id ++ \"\\n\"'"
        )
        assert result.returncode == 0, f"jj log failed: {result.stderr}"
        lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
        assert len(lines) == 1, (
            f"Expected exactly 1 commit for '{desc}', got {len(lines)}: {result.stdout}"
        )


def test_feature_auth_bookmark_exists():
    """Bookmark 'feature/auth' exists."""
    result = run("jj bookmark list")
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature/auth" in result.stdout, (
        f"Bookmark 'feature/auth' not found. Got: {result.stdout!r}"
    )


def test_feature_auth_bookmark_points_to_login_commit():
    """Bookmark 'feature/auth' points to the 'feat: implement user login' commit."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"feature/auth\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: implement user login" in result.stdout, (
        f"Bookmark 'feature/auth' should point to login commit. Got: {result.stdout!r}"
    )


def test_no_feature_password_reset_bookmark():
    """Bookmark 'feature/password-reset' does NOT exist in the initial state."""
    result = run("jj bookmark list")
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature/password-reset" not in result.stdout, (
        f"Bookmark 'feature/password-reset' should not exist yet. Got: {result.stdout!r}"
    )


def test_working_copy_is_empty():
    """The working copy commit has no file changes."""
    result = run("jj diff -r @")
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Working copy is not empty. Diff: {result.stdout}"
    )


def test_working_copy_parent_is_password_reset_commit():
    """The parent of the working copy is the 'feat: implement password reset' commit."""
    result = run(
        "jj log --no-graph -r '@-' -T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: implement password reset" in result.stdout, (
        f"Working copy parent should be password reset commit. Got: {result.stdout!r}"
    )


def test_src_login_py_in_login_commit():
    """src/login.py is tracked in the 'feat: implement user login' commit."""
    result = run(
        "jj file list -r 'description(substring:\"feat: implement user login\")'"
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "src/login.py" in result.stdout, (
        f"src/login.py not found in login commit. Files: {result.stdout}"
    )


def test_src_reset_py_in_password_reset_commit():
    """src/reset.py is tracked in the 'feat: implement password reset' commit."""
    result = run(
        "jj file list -r 'description(substring:\"feat: implement password reset\")'"
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "src/reset.py" in result.stdout, (
        f"src/reset.py not found in password reset commit. Files: {result.stdout}"
    )

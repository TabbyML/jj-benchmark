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
        "README.md not found in webapp repo"
    )


def test_app_init_py_exists():
    assert os.path.isfile(os.path.join(REPO_DIR, "app", "__init__.py")), (
        "app/__init__.py not found in webapp repo"
    )


def test_app_routes_py_exists():
    assert os.path.isfile(os.path.join(REPO_DIR, "app", "routes.py")), (
        "app/routes.py not found in webapp repo"
    )


def test_app_contact_py_exists():
    assert os.path.isfile(os.path.join(REPO_DIR, "app", "contact.py")), (
        "app/contact.py not found in webapp repo"
    )


def test_root_commit_exists():
    """Commit with 'chore: init webapp' description exists."""
    result = run(
        "jj log --no-graph -r 'description(substring:\"chore: init webapp\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "chore: init webapp" in result.stdout, (
        f"Root commit not found. Got: {result.stdout!r}"
    )


def test_homepage_commit_exists():
    """Commit with 'feat: add homepage route' description exists."""
    result = run(
        "jj log --no-graph -r 'description(substring:\"feat: add homepage route\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add homepage route" in result.stdout, (
        f"Homepage commit not found. Got: {result.stdout!r}"
    )


def test_contact_commit_exists():
    """Commit with 'feat: add contact page' description exists."""
    result = run(
        "jj log --no-graph -r 'description(substring:\"feat: add contact page\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add contact page" in result.stdout, (
        f"Contact commit not found. Got: {result.stdout!r}"
    )


def test_dev_bookmark_exists():
    """Bookmark 'dev' exists."""
    result = run("jj bookmark list")
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "dev" in result.stdout, (
        f"Bookmark 'dev' not found. Got: {result.stdout!r}"
    )


def test_dev_bookmark_points_to_homepage_commit():
    """Bookmark 'dev' points to the 'feat: add homepage route' commit."""
    result = run(
        "jj log --no-graph -r 'bookmarks(\"dev\")' "
        "-T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add homepage route" in result.stdout, (
        f"Bookmark 'dev' should point to homepage commit. Got: {result.stdout!r}"
    )


def test_no_feature_contact_bookmark():
    """Bookmark 'feature/contact' does NOT exist in the initial state."""
    result = run("jj bookmark list")
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature/contact" not in result.stdout, (
        f"Bookmark 'feature/contact' should not exist yet. Got: {result.stdout!r}"
    )


def test_working_copy_is_empty():
    """The working copy commit has no file changes."""
    result = run("jj diff -r @")
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Working copy is not empty. Diff: {result.stdout}"
    )


def test_working_copy_parent_is_contact_commit():
    """The parent of the working copy is the 'feat: add contact page' commit."""
    result = run(
        "jj log --no-graph -r '@-' -T 'description ++ \"\\n\"'"
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "feat: add contact page" in result.stdout, (
        f"Working copy parent should be contact commit. Got: {result.stdout!r}"
    )


def test_routes_py_in_homepage_commit():
    """app/routes.py is tracked in the 'feat: add homepage route' commit."""
    result = run(
        "jj file list -r 'description(substring:\"feat: add homepage route\")'"
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "app/routes.py" in result.stdout, (
        f"app/routes.py not found in homepage commit. Files: {result.stdout}"
    )


def test_contact_py_in_contact_commit():
    """app/contact.py is tracked in the 'feat: add contact page' commit."""
    result = run(
        "jj file list -r 'description(substring:\"feat: add contact page\")'"
    )
    assert result.returncode == 0, f"jj file list failed: {result.stderr}"
    assert "app/contact.py" in result.stdout, (
        f"app/contact.py not found in contact commit. Files: {result.stdout}"
    )

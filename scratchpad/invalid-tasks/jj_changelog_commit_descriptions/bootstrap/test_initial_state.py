import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/myrepo"


def test_jj_in_path():
    assert shutil.which("jj") is not None, "jj binary must be in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} must exist"


def test_repo_is_valid_jj_repo():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory must exist in {REPO_DIR}"
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_skeleton_py_file_exists():
    path = os.path.join(REPO_DIR, "skeleton.py")
    assert os.path.isfile(path), "skeleton.py must exist in the repo"


def test_readme_file_exists():
    path = os.path.join(REPO_DIR, "README.md")
    assert os.path.isfile(path), "README.md must exist in the repo"


def test_commit_chore_init_exists():
    result = subprocess.run(
        [
            "jj", "log", "--no-pager", "--no-graph",
            "-r", "description(substring:'chore(init): initialise project skeleton')",
            "--template", "description",
        ],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "chore(init): initialise project skeleton" in result.stdout, \
        "Commit 'chore(init): initialise project skeleton' must exist"


def test_commit_docs_readme_contributing_exists():
    result = subprocess.run(
        [
            "jj", "log", "--no-pager", "--no-graph",
            "-r", "description(substring:'docs(readme): add contributing guide')",
            "--template", "description",
        ],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "docs(readme): add contributing guide" in result.stdout, \
        "Commit 'docs(readme): add contributing guide' must exist in initial state"


def test_no_bookmarks_exist():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--no-pager"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert result.stdout.strip() == "", "There must be no bookmarks in the initial state"


def test_working_copy_has_no_description():
    result = subprocess.run(
        [
            "jj", "log", "--no-pager", "--no-graph",
            "-r", "@",
            "--template", "description",
        ],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log @ failed: {result.stderr}"
    assert result.stdout.strip() == "", "Working copy change must have an empty description initially"


def test_working_copy_parent_is_docs_readme():
    result = subprocess.run(
        [
            "jj", "log", "--no-pager", "--no-graph",
            "-r", "@-",
            "--template", "description",
        ],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log @- failed: {result.stderr}"
    assert "docs(readme): add contributing guide" in result.stdout, \
        "Parent of working copy must be 'docs(readme): add contributing guide'"


def test_changelog_md_does_not_exist_initially():
    path = os.path.join(REPO_DIR, "CHANGELOG.md")
    assert not os.path.isfile(path), "CHANGELOG.md must NOT exist in the initial state"

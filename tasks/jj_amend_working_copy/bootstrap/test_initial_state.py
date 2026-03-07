import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."


def test_repo_is_valid_jj_repo():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f"{REPO_DIR} is not a valid jj repository (.jj directory missing)."
    result = subprocess.run(["jj", "status"], cwd=REPO_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_readme_exists():
    path = os.path.join(REPO_DIR, "README.md")
    assert os.path.isfile(path), "README.md not found."
    assert "# My Project" in open(path).read(), "README.md missing '# My Project'."


def test_feature_py_exists():
    path = os.path.join(REPO_DIR, "feature.py")
    assert os.path.isfile(path), "feature.py not found."
    content = open(path).read()
    assert "def hello():" in content, "feature.py missing 'def hello():'."


def test_initial_commit_descriptions():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"'],
        cwd=REPO_DIR, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "chore: initial setup" in result.stdout, "'chore: initial setup' not in log."
    assert "wip: add feature" in result.stdout, "'wip: add feature' not in log."


def test_working_copy_is_wip():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "@", "-T", "description"],
        cwd=REPO_DIR, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "wip: add feature" in result.stdout, f"Working copy should be 'wip: add feature', got: {result.stdout.strip()}"

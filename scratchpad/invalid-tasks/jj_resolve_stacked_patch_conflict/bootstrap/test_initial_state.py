import os
import subprocess

REPO_DIR = "/home/user/upstream-project"


def test_jj_binary_in_path():
    result = subprocess.run(
        ["which", "jj"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist"


def test_jj_directory_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status", "--no-pager"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_src_data_py_exists():
    path = os.path.join(REPO_DIR, "src", "data.py")
    assert os.path.isfile(path), f"src/data.py does not exist in {REPO_DIR}"


def test_main_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--no-pager"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, "Bookmark 'main' not found"


def test_feature_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--no-pager"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "feature" in result.stdout, "Bookmark 'feature' not found"


def test_main_v2_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list", "--no-pager"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main-v2" in result.stdout, "Bookmark 'main-v2' not found"


def test_log_has_multiple_commits():
    result = subprocess.run(
        ["jj", "log", "--no-pager", "-r", "::@"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l for l in result.stdout.splitlines() if l.strip()]
    assert len(lines) >= 4, "Expected at least 4 commits in history"


def test_src_directory_exists():
    src_dir = os.path.join(REPO_DIR, "src")
    assert os.path.isdir(src_dir), f"src/ directory does not exist in {REPO_DIR}"

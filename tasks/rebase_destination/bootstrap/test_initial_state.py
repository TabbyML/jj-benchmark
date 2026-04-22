import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_jj_repo_initialized():
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), f"Jujutsu repository not initialized in {PROJECT_DIR}."

def test_bookmarks_exist():
    # Verify both 'main' and 'feature' bookmarks exist
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 0, "Failed to list jj bookmarks."
    output = result.stdout
    assert "main:" in output, "Bookmark 'main' does not exist."
    assert "feature:" in output, "Bookmark 'feature' does not exist."

import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_initial_commits_exist():
    # Verify that the repository is initialized and has the commits
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj log' failed: {result.stderr}"
    output = result.stdout
    assert "Add file B" in output, "Expected commit with description 'Add file B' in jj log."
    assert "Add file C" in output, "Expected commit with description 'Add file C' in jj log."

def test_initial_files_exist():
    # Verify that the files exist in the working directory
    b_txt_path = os.path.join(PROJECT_DIR, "b.txt")
    c_txt_path = os.path.join(PROJECT_DIR, "c.txt")
    assert os.path.isfile(b_txt_path), f"File {b_txt_path} does not exist."
    assert os.path.isfile(c_txt_path), f"File {c_txt_path} does not exist."

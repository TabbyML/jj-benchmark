import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_base_file_exists():
    file_path = os.path.join(PROJECT_DIR, "base.txt")
    assert os.path.isfile(file_path), f"File {file_path} does not exist."
    with open(file_path) as f:
        content = f.read().strip()
    assert content == "old", "Expected 'old' in base.txt."

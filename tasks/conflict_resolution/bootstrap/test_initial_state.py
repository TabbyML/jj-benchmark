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
    assert os.path.isdir(jj_dir), f"jj repository not initialized in {PROJECT_DIR}."

def test_file_exists():
    file_path = os.path.join(PROJECT_DIR, "file.txt")
    assert os.path.isfile(file_path), f"file.txt not found in {PROJECT_DIR}."

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
    assert os.path.isdir(jj_dir), "The directory is not a jj repository (.jj not found)."

def test_file_txt_exists():
    file_path = os.path.join(PROJECT_DIR, "file.txt")
    assert os.path.isfile(file_path), f"file.txt does not exist in {PROJECT_DIR}."

def test_conflict_markers_in_file():
    file_path = os.path.join(PROJECT_DIR, "file.txt")
    with open(file_path, "r") as f:
        content = f.read()
    assert "<<<<<<<" in content and ">>>>>>>" in content, "file.txt does not contain conflict markers."

def test_jj_status_shows_conflict():
    result = subprocess.run(["jj", "status"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert "unresolved conflicts" in result.stdout or "unresolved conflicts" in result.stderr, \
        "jj status does not indicate unresolved conflicts."

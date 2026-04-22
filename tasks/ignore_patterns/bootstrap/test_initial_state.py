import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_is_jj_repository():
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), f"Jujutsu repository not initialized in {PROJECT_DIR}."

def test_debug_log_exists():
    log_path = os.path.join(PROJECT_DIR, "debug.log")
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

def test_debug_log_is_tracked():
    result = subprocess.run(
        ["jj", "-R", PROJECT_DIR, "file", "list"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to list jj files: {result.stderr}"
    assert any(line.endswith("debug.log") for line in result.stdout.splitlines()), "debug.log is not tracked by jj initially."

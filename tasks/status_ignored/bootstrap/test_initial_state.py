import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_build_log_exists():
    log_path = os.path.join(PROJECT_DIR, "build.log")
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

def test_build_log_is_tracked():
    result = subprocess.run(
        ["jj", "file", "list"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj file list' failed: {result.stderr}"
    assert "build.log\n" in result.stdout or "build.log" in result.stdout.splitlines(), \
        "Expected build.log to be tracked by jj initially."

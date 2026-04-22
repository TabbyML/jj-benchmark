import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_main_py_exists():
    main_py_path = os.path.join(PROJECT_DIR, "main.py")
    assert os.path.isfile(main_py_path), f"File {main_py_path} does not exist."

def test_main_py_content():
    main_py_path = os.path.join(PROJECT_DIR, "main.py")
    with open(main_py_path) as f:
        content = f.read()
    assert "def foo():" in content, "Expected 'def foo():' in main.py."
    assert "def bar():" in content, "Expected 'def bar():' in main.py."
    assert "def hello():" in content, "Expected 'def hello():' in main.py."

def test_jj_repo_initialized():
    # Verify that the directory is a jj repository
    result = subprocess.run(["jj", "status"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"jj status failed, not a jj repository. Error: {result.stderr}"
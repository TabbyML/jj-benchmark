import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_main_py_content():
    main_py_path = os.path.join(PROJECT_DIR, "main.py")
    with open(main_py_path) as f:
        content = f.read()
    
    assert "def hello():" in content, "Expected 'def hello():' in main.py."
    assert "def bar():" in content, "Expected 'def bar():' in main.py."
    assert "def foo():" not in content, "Expected 'def foo():' to be removed from main.py."

def test_jj_diff():
    # Verify that the working copy diff only adds bar()
    result = subprocess.run(["jj", "diff", "--git"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"jj diff failed. Error: {result.stderr}"
    
    diff_output = result.stdout
    assert "+def bar():" in diff_output, "Expected jj diff to show addition of 'def bar():'."
    assert "+def foo():" not in diff_output, "Expected jj diff to NOT show addition of 'def foo():'."

def test_parent_commit_content():
    # The parent commit should still only have hello()
    result = subprocess.run(["jj", "file", "show", "main.py", "-r", "@-"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"jj file show failed. Error: {result.stderr}"
    
    parent_content = result.stdout
    assert "def hello():" in parent_content, "Expected parent commit to contain 'def hello():'."
    assert "def foo():" not in parent_content, "Expected parent commit to NOT contain 'def foo():'."
    assert "def bar():" not in parent_content, "Expected parent commit to NOT contain 'def bar():'."

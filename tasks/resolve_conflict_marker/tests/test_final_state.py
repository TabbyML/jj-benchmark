import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_file_txt_content():
    file_path = os.path.join(PROJECT_DIR, "file.txt")
    assert os.path.isfile(file_path), f"{file_path} does not exist."
    
    with open(file_path, "r") as f:
        content = f.read()
    
    expected_content = "A and B\n"
    assert content == expected_content, f"Expected file.txt to contain exactly {repr(expected_content)}, but got {repr(content)}"

def test_jj_status_no_conflicts():
    result = subprocess.run(["jj", "status"], cwd=PROJECT_DIR, capture_output=True, text=True)
    
    # Check both stdout and stderr for unresolved conflicts warning
    assert "unresolved conflicts" not in result.stdout.lower(), "jj status still shows unresolved conflicts in stdout."
    assert "unresolved conflicts" not in result.stderr.lower(), "jj status still shows unresolved conflicts in stderr."

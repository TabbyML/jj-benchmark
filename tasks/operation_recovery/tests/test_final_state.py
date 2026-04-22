import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_file1_and_file2_exist():
    assert os.path.isfile(os.path.join(PROJECT_DIR, "file1.txt")), "file1.txt should exist."
    assert os.path.isfile(os.path.join(PROJECT_DIR, "file2.txt")), "file2.txt should exist."

def test_file3_to_file5_absent():
    assert not os.path.exists(os.path.join(PROJECT_DIR, "file3.txt")), "file3.txt should not exist."
    assert not os.path.exists(os.path.join(PROJECT_DIR, "file4.txt")), "file4.txt should not exist."
    assert not os.path.exists(os.path.join(PROJECT_DIR, "file5.txt")), "file5.txt should not exist."

def test_jj_log_does_not_contain_commit_5():
    result = subprocess.run(
        ["jj", "log"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj log' failed: {result.stderr}"
    assert "Commit 5" not in result.stdout, "Expected 'Commit 5' to be reverted."
    assert "Commit 2" in result.stdout, "Expected 'Commit 2' to be present."
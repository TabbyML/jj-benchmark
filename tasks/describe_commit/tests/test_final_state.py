import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_commit_description():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "@", "-T", "description"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    description = result.stdout.strip()
    assert description == "feat: add new feature", f"Expected description 'feat: add new feature', but got '{description}'"

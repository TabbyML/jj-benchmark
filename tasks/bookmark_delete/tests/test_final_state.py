import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_bookmark_deleted():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    assert "feature-x" not in result.stdout, "Bookmark 'feature-x' was not deleted."

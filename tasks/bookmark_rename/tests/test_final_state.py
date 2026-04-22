import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_bookmark_renamed():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert "new-feature" in result.stdout, "Expected bookmark 'new-feature' to exist after renaming."
    assert "old-feature" not in result.stdout, "Expected bookmark 'old-feature' to no longer exist after renaming."

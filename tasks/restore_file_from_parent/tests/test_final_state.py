import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_config_restored():
    config_path = os.path.join(PROJECT_DIR, "config.txt")
    with open(config_path) as f:
        content = f.read()
    assert "port=8080" in content, "config.txt was not restored to the parent commit's state."

def test_app_not_restored():
    app_path = os.path.join(PROJECT_DIR, "app.py")
    with open(app_path) as f:
        content = f.read()
    assert "Hello World - v2" in content, "app.py was incorrectly modified or restored."

def test_jj_diff():
    result = subprocess.run(["jj", "diff"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0
    assert "config.txt" not in result.stdout, "config.txt still shows changes in jj diff."
    assert "app.py" in result.stdout, "app.py does not show changes in jj diff."

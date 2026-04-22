import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_commits_squashed():
    # Verify that "add feature A and B" exists, and "add feature A" / "add feature B" do not.
    result = subprocess.run(
        ["jj", "log", "-T", "description ++ \"\\n\"", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    output = result.stdout
    lines = [line.strip() for line in output.split('\n') if line.strip()]
    
    assert "add feature A and B" in lines, "Exact description 'add feature A and B' not found."
    assert "add feature C" in lines, "Exact description 'add feature C' not found."
    assert "add feature A" not in lines, "The original commit 'add feature A' is still present."
    assert "add feature B" not in lines, "The original commit 'add feature B' is still present."

def test_file_contents():
    # Verify that app.py contains all features
    app_py_path = os.path.join(PROJECT_DIR, "app.py")
    with open(app_py_path, "r") as f:
        content = f.read()
        
    assert "def feature_a(): pass" in content, "feature_a is missing from app.py"
    assert "def feature_b(): pass" in content, "feature_b is missing from app.py"
    assert "def feature_c(): pass" in content, "feature_c is missing from app.py"

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "get_author.sh")

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_output():
    try:
        output = subprocess.check_output(
            ["./get_author.sh"],
            cwd=PROJECT_DIR,
            text=True,
        )
        assert output == "Author: Test User <test@example.com>\n", f"Unexpected output: {repr(output)}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed: {e}")

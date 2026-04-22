import os
import shutil

def test_jj_installed():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_user_home_exists():
    assert os.path.isdir("/home/user"), "/home/user directory does not exist."

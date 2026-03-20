import os
import shutil
import subprocess
import pytest

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_repo_does_not_exist_yet():
    assert not os.path.exists("/home/user/secure_repo"), "Repository directory should not exist yet."

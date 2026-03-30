import os
import shutil
import pytest

def test_wasp_cli_installed():
    assert shutil.which("wasp") is not None, "Wasp CLI is not installed in the environment."

def test_home_directory_exists():
    assert os.path.isdir("/home/user"), "The home directory /home/user does not exist."

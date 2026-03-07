import os
import shutil
import subprocess
import pytest

HOME = "/home/user"
REPO_PATH = os.path.join(HOME, "myrepo")
CONFIG_PATH = os.path.join(HOME, ".config", "jj", "config.toml")


def test_jj_binary_exists():
    assert shutil.which("jj") is not None, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_PATH), f"Repo directory {REPO_PATH} does not exist"


def test_repo_is_valid_jj_repo():
    jj_dir = os.path.join(REPO_PATH, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_PATH}"


def test_jj_status_succeeds_in_repo():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_PATH,
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": HOME},
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_config_file_exists():
    assert os.path.isfile(CONFIG_PATH), f"Config file not found at {CONFIG_PATH}"


def test_config_file_has_user_name():
    with open(CONFIG_PATH, "r") as f:
        content = f.read()
    assert "Dev User" in content, "user.name 'Dev User' not found in config file"


def test_config_file_has_user_email():
    with open(CONFIG_PATH, "r") as f:
        content = f.read()
    assert "dev@example.com" in content, "user.email 'dev@example.com' not found in config file"


def test_no_aliases_section_preconfigured():
    with open(CONFIG_PATH, "r") as f:
        content = f.read()
    assert "aliases" not in content, "aliases section should not be pre-configured"


def test_no_ui_paginate_preconfigured():
    with open(CONFIG_PATH, "r") as f:
        content = f.read()
    assert "paginate" not in content, "ui.paginate should not be pre-configured"

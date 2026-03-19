import os
import shutil
import subprocess
import pytest

HOME_DIR = "/home/user"
REPO_DIR = "/home/user/myproject"


def test_jj_binary_in_path():
    assert shutil.which("jj") is not None, "jj binary not found in PATH"


def test_home_directory_exists():
    assert os.path.isdir(HOME_DIR), f"Home directory {HOME_DIR} does not exist"


def test_myproject_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Directory {REPO_DIR} does not exist"


def test_readme_exists():
    readme = os.path.join(REPO_DIR, "README.md")
    assert os.path.isfile(readme), f"README.md not found at {readme}"


def test_readme_content():
    readme = os.path.join(REPO_DIR, "README.md")
    with open(readme) as f:
        content = f.read()
    assert content.strip() == "# My Project", (
        f"README.md content mismatch: got '{content.strip()}'"
    )


def test_no_jj_repo_in_myproject():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert not os.path.exists(dot_jj), (
        f"{dot_jj} already exists; the user must initialise the jj repo"
    )


def test_no_jj_user_config():
    config_path = os.path.join(HOME_DIR, ".config", "jj", "config.toml")
    legacy_path = os.path.join(HOME_DIR, ".jjconfig.toml")
    assert not os.path.isfile(config_path), (
        f"User-level jj config already exists at {config_path}; "
        "the initial state should have no user config"
    )
    assert not os.path.isfile(legacy_path), (
        f"Legacy jj config already exists at {legacy_path}; "
        "the initial state should have no user config"
    )

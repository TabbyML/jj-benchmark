import os
import subprocess
import pytest

HOME_DIR = "/home/user"
REPO_DIR = "/home/user/myrepo"
JJ_BIN = "jj"


def test_jj_binary_exists():
    result = subprocess.run(["which", JJ_BIN], capture_output=True, text=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist"


def test_repo_is_valid_jj_repo():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"


def test_repo_has_at_least_one_commit():
    result = subprocess.run(
        [JJ_BIN, "log", "--no-graph", "--limit", "1"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": HOME_DIR},
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert result.stdout.strip(), "Repository has no commits"


def test_home_directory_exists():
    assert os.path.isdir(HOME_DIR), f"Home directory {HOME_DIR} does not exist"


def test_no_user_config_aliases_preset():
    config_path = os.path.join(HOME_DIR, ".config", "jj", "config.toml")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            content = f.read()
        assert "aliases" not in content, (
            "User config already has aliases set — initial state is not clean"
        )

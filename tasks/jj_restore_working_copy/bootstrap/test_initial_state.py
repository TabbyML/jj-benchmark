import os
import shutil
import subprocess
import pytest

REPO_DIR = "/home/user/project"


def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist."


def test_repo_is_valid_jj_repo():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), f"{REPO_DIR} is not a valid jj repository (.jj directory missing)."
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed in {REPO_DIR}: {result.stderr}"


def test_config_toml_exists():
    config_path = os.path.join(REPO_DIR, "config.toml")
    assert os.path.isfile(config_path), f"config.toml not found at {config_path}."


def test_config_toml_content():
    config_path = os.path.join(REPO_DIR, "config.toml")
    content = open(config_path).read()
    assert "[settings]" in content, "config.toml missing '[settings]' section."
    assert "version = 1" in content, "config.toml missing 'version = 1'."


def test_parser_py_exists():
    parser_path = os.path.join(REPO_DIR, "parser.py")
    assert os.path.isfile(parser_path), f"parser.py not found at {parser_path}."


def test_parser_py_has_upper_content():
    parser_path = os.path.join(REPO_DIR, "parser.py")
    content = open(parser_path).read()
    assert "return text.upper()" in content, (
        "parser.py should contain 'return text.upper()' as part of the wip refactor starting state."
    )


def test_initial_commit_descriptions_present():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    log = result.stdout
    assert "chore: add config" in log, "Expected commit 'chore: add config' not found in log."
    assert "feat: add parser" in log, "Expected commit 'feat: add parser' not found in log."
    assert "wip: partial refactor" in log, "Expected commit 'wip: partial refactor' not found in log."


def test_working_copy_is_wip_refactor():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-r", "@", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "wip: partial refactor" in result.stdout, (
        f"Working copy description should be 'wip: partial refactor', got: {result.stdout.strip()}"
    )

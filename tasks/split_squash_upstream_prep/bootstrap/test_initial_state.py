import os
import subprocess
import pytest

REPO_DIR = "/home/user/mylib"


def test_jj_binary_in_path():
    result = subprocess.run(
        ["which", "jj"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_dir_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory does not exist: {REPO_DIR}"


def test_repo_is_valid_jj_repo():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found inside {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_readme_exists():
    readme_path = os.path.join(REPO_DIR, "README.md")
    assert os.path.isfile(readme_path), f"README.md not found at {readme_path}"


def test_readme_content():
    readme_path = os.path.join(REPO_DIR, "README.md")
    with open(readme_path) as f:
        content = f.read()
    assert "mylib" in content, f"README.md does not contain 'mylib'. Content: {content!r}"


def test_src_utils_py_exists():
    utils_path = os.path.join(REPO_DIR, "src", "utils.py")
    assert os.path.isfile(utils_path), f"src/utils.py not found at {utils_path}"


def test_src_config_py_exists():
    config_path = os.path.join(REPO_DIR, "src", "config.py")
    assert os.path.isfile(config_path), f"src/config.py not found at {config_path}"


def test_tests_test_config_py_exists():
    test_path = os.path.join(REPO_DIR, "tests", "test_config.py")
    assert os.path.isfile(test_path), f"tests/test_config.py not found at {test_path}"


def test_src_utils_py_content():
    utils_path = os.path.join(REPO_DIR, "src", "utils.py")
    with open(utils_path) as f:
        content = f.read()
    assert "def greet" in content, f"src/utils.py missing 'def greet'. Content: {content!r}"
    assert "Hello" in content, f"src/utils.py missing greeting. Content: {content!r}"


def test_src_config_py_content():
    config_path = os.path.join(REPO_DIR, "src", "config.py")
    with open(config_path) as f:
        content = f.read()
    assert "def parse_config" in content, f"src/config.py missing 'def parse_config'. Content: {content!r}"


def test_tests_test_config_py_content():
    test_path = os.path.join(REPO_DIR, "tests", "test_config.py")
    with open(test_path) as f:
        content = f.read()
    assert "def test_parse_config" in content, f"tests/test_config.py missing 'def test_parse_config'. Content: {content!r}"


def test_mixed_commit_exists():
    result = subprocess.run(
        ["jj", "log", "-r", 'description(substring:"add config parser and update tests")',
         "--no-graph", "-T", 'description ++ "\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add config parser and update tests" in result.stdout, (
        f"Expected commit 'add config parser and update tests' not found. stdout: {result.stdout!r}"
    )


def test_initial_commit_exists():
    result = subprocess.run(
        ["jj", "log", "-r", 'description(substring:"initial commit")',
         "--no-graph", "-T", 'description ++ "\n"'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "initial commit" in result.stdout, (
        f"Expected 'initial commit' not found. stdout: {result.stdout!r}"
    )


def test_working_copy_is_empty():
    result = subprocess.run(
        ["jj", "diff", "--summary"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Working copy should be empty but has changes: {result.stdout!r}"
    )

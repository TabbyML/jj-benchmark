import os
import subprocess
import pytest

REPO_DIR = "/home/user/project"


def test_jj_binary_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True, text=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_dir_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist"


def test_repo_is_jj_repo():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}; not a valid jj repo"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj status failed in {REPO_DIR}: {result.stderr}"


def test_readme_file_exists_in_initial_scaffold_commit():
    result = subprocess.run(
        ["jj", "file", "show", "-r", 'description(substring:"initial project scaffold")', "README.md"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"README.md not found in 'initial project scaffold' commit: {result.stderr}"
    )
    assert "# MyProject" in result.stdout, (
        "README.md in 'initial project scaffold' does not contain '# MyProject'"
    )


def test_auth_module_commit_absent_after_abandon():
    # After the accidental abandon, "add user authentication module" commit
    # should NOT be visible in standard jj log (it was abandoned/hidden).
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description",
         "-r", 'description(substring:"add user authentication module")'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    # Either non-zero exit or empty output means the commit is not visible
    assert result.returncode != 0 or result.stdout.strip() == "", (
        "Expected 'add user authentication module' commit to be absent (abandoned) in initial state, "
        f"but it was found: stdout={result.stdout!r}"
    )


def test_update_readme_commit_exists():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description",
         "-r", 'description(substring:"update README with usage instructions")'],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"'update README with usage instructions' commit not found: {result.stderr}"
    )
    assert "update README with usage instructions" in result.stdout, (
        "'update README with usage instructions' commit description not found in log output"
    )


def test_readme_updated_content_in_update_commit():
    result = subprocess.run(
        ["jj", "file", "show", "-r", 'description(substring:"update README with usage instructions")', "README.md"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"README.md not found in 'update README with usage instructions' commit: {result.stderr}"
    )
    assert "## Usage" in result.stdout, (
        "README.md in 'update README with usage instructions' does not contain '## Usage'"
    )


def test_src_auth_py_absent_in_working_copy():
    # After the abandon, the working copy should not contain src/auth.py
    auth_py = os.path.join(REPO_DIR, "src", "auth.py")
    assert not os.path.isfile(auth_py), (
        f"src/auth.py should not exist in working copy after accidental abandon, "
        f"but it does at {auth_py}"
    )


def test_main_bookmark_exists():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "main" in result.stdout, "Bookmark 'main' not found in initial state"


def test_operation_log_contains_abandon():
    result = subprocess.run(
        ["jj", "op", "log", "--no-graph", "-T", "description"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"jj op log failed: {result.stderr}"
    assert "abandon" in result.stdout.lower(), (
        "Expected to find an 'abandon' operation in the operation log, "
        f"but got: {result.stdout!r}"
    )

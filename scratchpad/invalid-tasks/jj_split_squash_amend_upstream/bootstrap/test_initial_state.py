import os
import subprocess
import pytest

REPO_DIR = "/home/user/myproject"


def test_jj_binary_in_path():
    result = subprocess.run(
        ["which", "jj"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO_DIR), f"Repository directory {REPO_DIR} does not exist"


def test_jj_directory_exists():
    jj_dir = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {REPO_DIR}"


def test_jj_status_succeeds():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_readme_exists():
    path = os.path.join(REPO_DIR, "README.md")
    assert os.path.isfile(path), f"README.md not found at {path}"


def test_cargo_toml_exists():
    path = os.path.join(REPO_DIR, "Cargo.toml")
    assert os.path.isfile(path), f"Cargo.toml not found at {path}"


def test_src_parser_rs_exists():
    path = os.path.join(REPO_DIR, "src", "parser.rs")
    assert os.path.isfile(path), f"src/parser.rs not found at {path}"


def test_src_http_rs_exists():
    path = os.path.join(REPO_DIR, "src", "http.rs")
    assert os.path.isfile(path), f"src/http.rs not found at {path}"


def test_src_lib_rs_exists():
    path = os.path.join(REPO_DIR, "src", "lib.rs")
    assert os.path.isfile(path), f"src/lib.rs not found at {path}"


def test_commit_add_parser_and_http_client_exists():
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", 'description ++ "\n"',
            "-r", 'description(substring:"add parser and http client")',
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add parser and http client" in result.stdout, (
        "Expected commit 'add parser and http client' not found"
    )


def test_commit_fix_debug_print_exists():
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", 'description ++ "\n"',
            "-r", 'description(substring:"fix: forgot to remove debug print")',
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "fix: forgot to remove debug print" in result.stdout, (
        "Expected commit 'fix: forgot to remove debug print' not found"
    )


def test_commit_init_scaffold_exists():
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", 'description ++ "\n"',
            "-r", 'description(substring:"init: scaffold project structure")',
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "init: scaffold project structure" in result.stdout, (
        "Expected commit 'init: scaffold project structure' not found"
    )


def test_working_copy_is_empty():
    result = subprocess.run(
        ["jj", "diff", "--summary"],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj diff failed: {result.stderr}"
    assert result.stdout.strip() == "", (
        f"Working copy should be empty but has changes: {result.stdout}"
    )


def test_mutable_commit_count_is_four():
    # Count commits using jj log with change_id template to get one line per commit
    result = subprocess.run(
        [
            "jj", "log", "--no-graph",
            "-T", 'change_id ++ "\n"',
            "-r", "mutable()",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    lines = [l for l in result.stdout.splitlines() if l.strip()]
    assert len(lines) == 4, (
        f"Expected 4 mutable commits (init, add parser and http client, fix, empty wc), "
        f"got {len(lines)}: {result.stdout}"
    )

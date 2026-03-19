import os
import subprocess
import pytest

REPO = "/home/user/widget-engine"


def run(cmd, cwd=None):
    result = subprocess.run(["jj", "--no-pager"] + list(cmd), capture_output=True, text=True, cwd=cwd)
    return result


def test_jj_binary_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True, text=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir(REPO), f"Repo directory {REPO} does not exist"


def test_jj_dir_exists():
    assert os.path.isdir(os.path.join(REPO, ".jj")), ".jj directory not found in repo"


def test_jj_status_succeeds():
    result = run(["status"], cwd=REPO)
    assert result.returncode == 0, f"jj status failed: {result.stderr}"


def test_src_dir_exists():
    assert os.path.isdir(os.path.join(REPO, "src")), "src/ directory does not exist"


def test_src_api_py_exists():
    assert os.path.isfile(os.path.join(REPO, "src", "api.py")), "src/api.py does not exist"


def test_src_auth_py_exists():
    assert os.path.isfile(os.path.join(REPO, "src", "auth.py")), "src/auth.py does not exist"


def test_release_notes_exists():
    assert os.path.isfile(os.path.join(REPO, "RELEASE_NOTES.md")), "RELEASE_NOTES.md does not exist"


def test_version_txt_exists():
    assert os.path.isfile(os.path.join(REPO, "version.txt")), "version.txt does not exist"


def test_bookmark_release_v23_exists():
    result = run(["bookmark", "list"], cwd=REPO)
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "release/v2.3" in result.stdout, "Bookmark release/v2.3 not found"


def test_commit_initial_project_scaffold_exists():
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"initial project scaffold")'],
        cwd=REPO,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "initial project scaffold" in result.stdout


def test_commit_mixed_api_and_auth_exists():
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"add API endpoint and fix login bug")'],
        cwd=REPO,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add API endpoint and fix login bug" in result.stdout


def test_commit_add_release_notes_exists():
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"add release notes")'],
        cwd=REPO,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "add release notes" in result.stdout


def test_commit_wip_bump_version_exists():
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"wip: bump version")'],
        cwd=REPO,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "wip: bump version" in result.stdout


def test_commit_fixup_release_notes_exists():
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"',
         "-r", 'description(substring:"fixup: missing newline in release notes")'],
        cwd=REPO,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    assert "fixup: missing newline in release notes" in result.stdout


def test_mixed_commit_contains_api_and_auth():
    result = run(
        ["show", "--name-only",
         "-r", 'description(substring:"add API endpoint and fix login bug")'],
        cwd=REPO,
    )
    assert result.returncode == 0, f"jj show failed: {result.stderr}"
    assert "src/api.py" in result.stdout
    assert "src/auth.py" in result.stdout


def test_five_non_root_commits():
    result = run(
        ["log", "--no-graph", "-T", 'description ++ "\\n"', "-r", "root()..@"],
        cwd=REPO,
    )
    assert result.returncode == 0, f"jj log failed: {result.stderr}"
    # jj log shows newest first; count non-empty lines
    descriptions = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    assert len(descriptions) == 5, f"Expected 5 commits, got {len(descriptions)}: {descriptions}"

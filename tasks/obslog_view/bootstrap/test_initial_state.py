import os
import shutil
import subprocess

def test_jj_installed():
    assert shutil.which("jj") is not None, "jj executable not found in PATH"

def test_repo_exists():
    repo_path = "/home/user/repo"
    assert os.path.isdir(repo_path), f"Repository directory {repo_path} does not exist"
    assert os.path.isdir(os.path.join(repo_path, ".jj")), f"jj repository not initialized in {repo_path}"

def test_obslog_has_history():
    repo_path = "/home/user/repo"
    result = subprocess.run(
        ["jj", "obslog", "--no-graph"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True
    )
    lines = result.stdout.strip().split('\n')
    # There should be at least 2 entries in the obslog to be meaningful
    assert len(lines) >= 2, "Expected at least 2 entries in the obslog for the current commit"

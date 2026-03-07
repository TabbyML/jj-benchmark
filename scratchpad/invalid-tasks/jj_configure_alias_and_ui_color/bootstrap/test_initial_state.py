import os
import subprocess


def test_jj_binary_in_path():
    result = subprocess.run(
        ["which", "jj"],
        capture_output=True,
    )
    assert result.returncode == 0, "jj binary not found in PATH"


def test_myrepo_directory_exists():
    repo_path = "/home/user/myrepo"
    assert os.path.isdir(repo_path), f"Directory {repo_path} does not exist"


def test_myrepo_has_jj_directory():
    jj_path = "/home/user/myrepo/.jj"
    assert os.path.isdir(jj_path), f".jj directory not found at {jj_path}"


def test_jj_status_succeeds_in_myrepo():
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        cwd="/home/user/myrepo",
    )
    assert result.returncode == 0, (
        f"jj status failed in /home/user/myrepo: {result.stderr.decode()}"
    )


def test_myrepo_has_at_least_one_commit():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "commit_id", "--limit", "1"],
        capture_output=True,
        cwd="/home/user/myrepo",
    )
    assert result.returncode == 0, (
        f"jj log failed in /home/user/myrepo: {result.stderr.decode()}"
    )
    output = result.stdout.decode().strip()
    assert len(output) > 0, "No commits found in /home/user/myrepo"

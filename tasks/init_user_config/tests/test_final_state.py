import os
import subprocess
import pytest

HOME_DIR = "/home/user"
REPO_DIR = "/home/user/myproject"


def run_jj(args, cwd=None):
    env = {**os.environ, "HOME": HOME_DIR}
    return subprocess.run(
        ["jj"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        env=env,
    )


def test_myproject_jj_directory_exists():
    dot_jj = os.path.join(REPO_DIR, ".jj")
    assert os.path.isdir(dot_jj), (
        f"{REPO_DIR}/.jj directory does not exist; "
        "jj git init must be run inside /home/user/myproject"
    )


def test_jj_status_succeeds():
    result = run_jj(["status"], cwd=REPO_DIR)
    assert result.returncode == 0, (
        f"jj status failed in {REPO_DIR}:\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_user_name_is_alex_developer():
    result = run_jj(["config", "get", "user.name"], cwd=REPO_DIR)
    assert result.returncode == 0, (
        f"jj config get user.name failed: {result.stderr}"
    )
    assert result.stdout.strip() == "Alex Developer", (
        f"user.name expected 'Alex Developer', got: '{result.stdout.strip()}'"
    )


def test_user_email_is_alex_at_example():
    result = run_jj(["config", "get", "user.email"], cwd=REPO_DIR)
    assert result.returncode == 0, (
        f"jj config get user.email failed: {result.stderr}"
    )
    assert result.stdout.strip() == "alex@example.com", (
        f"user.email expected 'alex@example.com', got: '{result.stdout.strip()}'"
    )


def test_user_name_is_user_level():
    result = run_jj(["config", "list", "--user", "user.name"], cwd=REPO_DIR)
    assert result.returncode == 0, (
        f"jj config list --user user.name failed: {result.stderr}"
    )
    assert "Alex Developer" in result.stdout, (
        f"user.name not found in user-level config. Output: '{result.stdout.strip()}'"
    )


def test_user_email_is_user_level():
    result = run_jj(["config", "list", "--user", "user.email"], cwd=REPO_DIR)
    assert result.returncode == 0, (
        f"jj config list --user user.email failed: {result.stderr}"
    )
    assert "alex@example.com" in result.stdout, (
        f"user.email not found in user-level config. Output: '{result.stdout.strip()}'"
    )


def test_readme_still_exists():
    readme = os.path.join(REPO_DIR, "README.md")
    assert os.path.isfile(readme), f"README.md missing from {REPO_DIR}"


def test_readme_content_unchanged():
    readme = os.path.join(REPO_DIR, "README.md")
    with open(readme) as f:
        content = f.read()
    assert content.strip() == "# My Project", (
        f"README.md content changed; expected '# My Project', got: '{content.strip()}'"
    )

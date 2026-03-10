import os
import subprocess


def test_jj_binary_in_path():
    result = subprocess.run(["which", "jj"], capture_output=True)
    assert result.returncode == 0, "jj binary not found in PATH"


def test_git_binary_in_path():
    result = subprocess.run(["which", "git"], capture_output=True)
    assert result.returncode == 0, "git binary not found in PATH"


def test_repo_directory_exists():
    assert os.path.isdir("/home/user/gitrepo"), "/home/user/gitrepo directory does not exist"


def test_repo_is_git_repo():
    git_dir = "/home/user/gitrepo/.git"
    assert os.path.isdir(git_dir), ".git directory does not exist — not a Git repo"


def test_jj_not_yet_initialized():
    jj_dir = "/home/user/gitrepo/.jj"
    assert not os.path.exists(jj_dir), ".jj directory already exists before task starts"


def test_git_readme_exists():
    readme = "/home/user/gitrepo/README.md"
    assert os.path.isfile(readme), "README.md not found in gitrepo"


def test_git_config_toml_exists():
    config = "/home/user/gitrepo/config.toml"
    assert os.path.isfile(config), "config.toml not found in gitrepo"


def test_git_main_branch_exists():
    result = subprocess.run(
        ["git", "-C", "/home/user/gitrepo", "branch", "--list", "main"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "git branch command failed"
    assert "main" in result.stdout, "'main' branch does not exist in gitrepo"


def test_git_has_two_commits():
    result = subprocess.run(
        ["git", "-C", "/home/user/gitrepo", "log", "--oneline"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "git log failed"
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
    assert len(lines) == 2, f"Expected 2 commits, found {len(lines)}"


def test_git_initial_commit_present():
    result = subprocess.run(
        ["git", "-C", "/home/user/gitrepo", "log", "--oneline"],
        capture_output=True,
        text=True,
    )
    assert "initial commit" in result.stdout, "'initial commit' not found in git log"


def test_git_add_config_commit_present():
    result = subprocess.run(
        ["git", "-C", "/home/user/gitrepo", "log", "--oneline"],
        capture_output=True,
        text=True,
    )
    assert "add config" in result.stdout, "'add config' commit not found in git log"

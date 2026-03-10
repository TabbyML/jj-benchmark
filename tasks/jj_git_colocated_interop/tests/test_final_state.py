import os
import subprocess


REPO = "/home/user/gitrepo"


def test_jj_dir_exists():
    """Colocated jj repo was initialized — .jj directory must exist."""
    assert os.path.isdir(os.path.join(REPO, ".jj")), \
        f".jj directory not found in {REPO} — did you run `jj git init --colocate`?"


def test_jj_status_succeeds():
    """jj status must exit 0 inside the repo."""
    result = subprocess.run(
        ["jj", "status"],
        capture_output=True,
        cwd=REPO,
    )
    assert result.returncode == 0, \
        f"`jj status` failed:\n{result.stderr.decode()}"


def test_notes_txt_exists():
    """notes.txt was created during the task."""
    path = os.path.join(REPO, "notes.txt")
    assert os.path.isfile(path), f"{path} does not exist"


def test_notes_txt_content():
    """notes.txt must contain 'interop test'."""
    path = os.path.join(REPO, "notes.txt")
    content = open(path).read()
    assert "interop test" in content, \
        f"Expected 'interop test' in notes.txt, got: {content!r}"


def test_notes2_txt_exists():
    """notes2.txt was created during the task."""
    path = os.path.join(REPO, "notes2.txt")
    assert os.path.isfile(path), f"{path} does not exist"


def test_notes2_txt_content():
    """notes2.txt must contain 'second note'."""
    path = os.path.join(REPO, "notes2.txt")
    content = open(path).read()
    assert "second note" in content, \
        f"Expected 'second note' in notes2.txt, got: {content!r}"


def test_add_notes_commit_present():
    """jj log must show a commit with description 'add notes'."""
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ \"\\n\"", "-r", "all()"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert result.returncode == 0, f"`jj log` failed:\n{result.stderr}"
    assert "add notes" in result.stdout, \
        f"Commit 'add notes' not found in jj log:\n{result.stdout}"


def test_add_notes2_commit_present():
    """jj log must show a commit with description 'add notes2'."""
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", "description ++ \"\\n\"", "-r", "all()"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert result.returncode == 0, f"`jj log` failed:\n{result.stderr}"
    assert "add notes2" in result.stdout, \
        f"Commit 'add notes2' not found in jj log:\n{result.stdout}"


def test_bookmark_feature_interop_deleted():
    """The 'feature/interop' bookmark must have been deleted in jj."""
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert result.returncode == 0, f"`jj bookmark list` failed:\n{result.stderr}"
    assert "feature/interop" not in result.stdout, \
        f"Bookmark 'feature/interop' still present in jj bookmark list:\n{result.stdout}"


def test_git_branch_feature_interop_deleted():
    """The 'feature/interop' Git branch must not exist after jj git export."""
    result = subprocess.run(
        ["git", "branch"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert result.returncode == 0, f"`git branch` failed:\n{result.stderr}"
    assert "feature/interop" not in result.stdout, \
        f"Git branch 'feature/interop' still present:\n{result.stdout}"


def test_jj_config_user_name():
    """jj repo-level config must have user.name = 'OS Engineer'."""
    result = subprocess.run(
        ["jj", "config", "get", "--repo", "user.name"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert result.returncode == 0, \
        f"`jj config get --repo user.name` failed:\n{result.stderr}"
    assert result.stdout.strip() == "OS Engineer", \
        f"Expected user.name='OS Engineer', got: {result.stdout.strip()!r}"


def test_jj_config_user_email():
    """jj repo-level config must have user.email = 'os@example.com'."""
    result = subprocess.run(
        ["jj", "config", "get", "--repo", "user.email"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert result.returncode == 0, \
        f"`jj config get --repo user.email` failed:\n{result.stderr}"
    assert result.stdout.strip() == "os@example.com", \
        f"Expected user.email='os@example.com', got: {result.stdout.strip()!r}"

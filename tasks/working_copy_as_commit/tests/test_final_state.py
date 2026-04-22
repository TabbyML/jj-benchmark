import os
import subprocess

def test_repo_exists():
    assert os.path.isdir("/home/user/repo/.jj"), "The jj repository was not initialized in /home/user/repo."

def test_hello_txt_exists():
    file_path = "/home/user/repo/hello.txt"
    assert os.path.isfile(file_path), "The file hello.txt does not exist."
    with open(file_path, "r") as f:
        content = f.read().strip()
    assert content == "Hello jj", f"Expected 'Hello jj' in hello.txt, got '{content}'."

def test_parent_commit_contains_hello():
    result = subprocess.run(
        ["jj", "log", "-r", "@-"],
        cwd="/home/user/repo",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to inspect parent commit (@-)."

def test_working_copy_is_empty():
    result = subprocess.run(
        ["jj", "st"],
        cwd="/home/user/repo",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run jj st."
    assert "The working copy has no changes." in result.stdout or "Working copy changes:" not in result.stdout, "The working copy is not empty. Did you forget to run `jj new`?"

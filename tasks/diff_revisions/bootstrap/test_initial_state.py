import os
import shutil
import subprocess

PROJECT_DIR = "/home/user/myproject"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_jj_repo_initialized():
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), f"Jujutsu repository not initialized in {PROJECT_DIR}."

def test_bookmarks_exist():
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    output = result.stdout
    assert "start" in output, "Bookmark 'start' does not exist."
    assert "middle" in output, "Bookmark 'middle' does not exist."
    assert "end" in output, "Bookmark 'end' does not exist."

def test_working_copy_content():
    with open(os.path.join(PROJECT_DIR, "hello.txt"), "r") as f:
        content = f.read().strip()
    assert content == "Hello World!!!", "Working copy hello.txt does not have the expected content."

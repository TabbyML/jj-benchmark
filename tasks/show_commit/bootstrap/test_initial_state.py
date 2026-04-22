import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_is_jj_repository():
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), f".jj directory not found in {PROJECT_DIR}."

def test_config_file_exists():
    config_path = os.path.join(PROJECT_DIR, "config.txt")
    assert os.path.isfile(config_path), f"File {config_path} does not exist."

def test_config_file_content():
    config_path = os.path.join(PROJECT_DIR, "config.txt")
    with open(config_path) as f:
        content = f.read()
    assert "key=new_value" in content, f"Expected 'key=new_value' in {config_path}."

def test_commits_exist():
    # Use jj log to check if the commits exist
    result = subprocess.run(
        ["jj", "log", "-r", "description(substring:\"Add configuration file\")", "-T", "description"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert "Add configuration file" in result.stdout, "Commit 'Add configuration file' not found."

    result = subprocess.run(
        ["jj", "log", "-r", "description(substring:\"Update configuration file\")", "-T", "description"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert "Update configuration file" in result.stdout, "Commit 'Update configuration file' not found."

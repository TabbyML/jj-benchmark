import os
import shutil
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_jj_binary_available():
    assert shutil.which("jj") is not None, "jj binary not found in PATH."

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_jj_repo_initialized():
    jj_dir = os.path.join(PROJECT_DIR, ".jj")
    assert os.path.isdir(jj_dir), f"jj repository not initialized in {PROJECT_DIR}."

def test_feature_files_exist():
    feature_a = os.path.join(PROJECT_DIR, "feature_a.py")
    feature_b = os.path.join(PROJECT_DIR, "feature_b.py")
    assert os.path.isfile(feature_a), f"File {feature_a} does not exist."
    assert os.path.isfile(feature_b), f"File {feature_b} does not exist."

def test_working_copy_has_changes():
    result = subprocess.run(
        ["jj", "st"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert "Working copy changes:" in result.stdout or "M feature_a.py" in result.stdout, "Working copy does not have changes to feature_a.py or feature_b.py."

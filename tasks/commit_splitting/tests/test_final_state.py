import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_combined_commit_absent():
    result = subprocess.run(
        ["jj", "log", "-T", "description"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert "Combined changes" not in result.stdout, "Expected 'Combined changes' commit to be split and removed."

def test_modify_fileA_commit_exists_and_contains_fileA():
    result = subprocess.run(
        ["jj", "log", "-r", "description(\"Modify fileA*\")", "-T", "description"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert "Modify fileA" in result.stdout, "Expected 'Modify fileA' commit to exist."

    diff_result = subprocess.run(
        ["jj", "diff", "-r", "description(\"Modify fileA*\")", "--stat"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert "fileA.txt" in diff_result.stdout, "Expected 'Modify fileA' commit to modify fileA.txt."
    assert "fileB.txt" not in diff_result.stdout, "Expected 'Modify fileA' commit to NOT modify fileB.txt."

def test_modify_fileB_commit_exists_and_contains_fileB():
    result = subprocess.run(
        ["jj", "log", "-r", "description(\"Modify fileB*\")", "-T", "description"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert "Modify fileB" in result.stdout, "Expected 'Modify fileB' commit to exist."

    diff_result = subprocess.run(
        ["jj", "diff", "-r", "description(\"Modify fileB*\")", "--stat"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert "fileB.txt" in diff_result.stdout, "Expected 'Modify fileB' commit to modify fileB.txt."
    assert "fileA.txt" not in diff_result.stdout, "Expected 'Modify fileB' commit to NOT modify fileA.txt."

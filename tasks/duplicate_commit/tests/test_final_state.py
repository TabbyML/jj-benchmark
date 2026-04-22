import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_duplicate_commit_exists_on_feature_b():
    # Find children of feature-b
    result = subprocess.run(
        ["jj", "log", "-r", "children(feature-b)", "-T", "description", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    # The duplicated commit should have the same description as feature-a
    assert "Feature A changes" in result.stdout, "The duplicated commit was not found as a child of feature-b."

def test_original_feature_a_intact():
    # feature-a should still exist and have its original parent (base)
    result = subprocess.run(
        ["jj", "log", "-r", "parents(feature-a)", "-T", "bookmarks", "--no-graph"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    assert "base" in result.stdout, "The original feature-a commit seems to have been modified or moved."
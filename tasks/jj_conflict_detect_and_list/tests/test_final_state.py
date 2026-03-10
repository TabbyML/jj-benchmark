import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_status_output_exists():
    path = os.path.join(REPO_DIR, "status_output.txt")
    assert os.path.isfile(path), "status_output.txt does not exist."


def test_conflict_list_exists():
    path = os.path.join(REPO_DIR, "conflict_list.txt")
    assert os.path.isfile(path), "conflict_list.txt does not exist."


def test_log_output_exists():
    path = os.path.join(REPO_DIR, "log_output.txt")
    assert os.path.isfile(path), "log_output.txt does not exist."


def test_conflict_list_contains_config_txt():
    path = os.path.join(REPO_DIR, "conflict_list.txt")
    content = open(path).read()
    assert "config.txt" in content, f"conflict_list.txt should contain 'config.txt'. Got: {content}"


def test_status_output_shows_conflict():
    path = os.path.join(REPO_DIR, "status_output.txt")
    content = open(path).read()
    assert "conflict" in content.lower() or "C " in content, \
        f"status_output.txt should show conflict. Got: {content}"


def test_log_output_contains_commits():
    path = os.path.join(REPO_DIR, "log_output.txt")
    content = open(path).read()
    assert "feat: feature change" in content or "main: main change" in content, \
        f"log_output.txt should contain commit descriptions. Got: {content}"

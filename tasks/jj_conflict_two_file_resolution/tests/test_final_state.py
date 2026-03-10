import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def test_conflicts_before_txt_exists():
    path = os.path.join(REPO_DIR, "conflicts_before.txt")
    assert os.path.isfile(path), "conflicts_before.txt does not exist."
    content = open(path).read()
    assert "server.cfg" in content and "client.cfg" in content, \
        f"conflicts_before.txt should list both files. Got: {content}"


def test_server_cfg_resolved():
    path = os.path.join(REPO_DIR, "server.cfg")
    content = open(path).read()
    assert "<<<<<<<" not in content, "server.cfg still has conflict markers."
    assert "host=prod.server.com" in content, f"server.cfg should have prod host. Got: {content}"
    assert "debug=true" in content, f"server.cfg should have debug=true. Got: {content}"


def test_client_cfg_resolved():
    path = os.path.join(REPO_DIR, "client.cfg")
    content = open(path).read()
    assert "<<<<<<<" not in content, "client.cfg still has conflict markers."
    assert "port=443" in content, f"client.cfg should have port=443. Got: {content}"
    assert "timeout=30" in content, f"client.cfg should have timeout=30. Got: {content}"


def test_no_conflicts_remain():
    result = subprocess.run(
        ["jj", "resolve", "--list"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "", f"Conflicts remain: {result.stdout}"


def test_conflicts_after_txt_empty():
    path = os.path.join(REPO_DIR, "conflicts_after.txt")
    assert os.path.isfile(path), "conflicts_after.txt does not exist."
    content = open(path).read().strip()
    assert content == "", f"conflicts_after.txt should be empty. Got: {content}"


def test_commit_description_updated():
    result = subprocess.run(
        ["jj", "log", "--no-graph", "-T", 'description ++ "\n"', "-r", "all()"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    assert "feat: feature configs (resolved)" in result.stdout, \
        f"Expected updated description. Got: {result.stdout}"

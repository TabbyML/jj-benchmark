import os
import json
import subprocess
import pytest

REPO_DIR = "/home/user/repo"


def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)


def test_ci_metadata_json_exists():
    assert os.path.isfile("/home/user/ci_metadata.json"), \
        "/home/user/ci_metadata.json does not exist."


def test_ci_metadata_is_valid_json():
    with open("/home/user/ci_metadata.json") as f:
        content = f.read()
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        pytest.fail(f"ci_metadata.json is not valid JSON: {e}")


def test_ci_metadata_has_commit_id():
    with open("/home/user/ci_metadata.json") as f:
        data = json.load(f)
    assert "commit_id" in data, "ci_metadata.json missing 'commit_id' field"
    assert isinstance(data["commit_id"], str) and len(data["commit_id"]) > 0, \
        "commit_id must be a non-empty string"
    assert all(c in "0123456789abcdef" for c in data["commit_id"].lower()), \
        f"commit_id should be hex, got: {data['commit_id']}"


def test_ci_metadata_has_change_id():
    with open("/home/user/ci_metadata.json") as f:
        data = json.load(f)
    assert "change_id" in data, "ci_metadata.json missing 'change_id' field"
    assert isinstance(data["change_id"], str) and len(data["change_id"]) > 0, \
        "change_id must be a non-empty string"


def test_ci_metadata_has_author():
    with open("/home/user/ci_metadata.json") as f:
        data = json.load(f)
    assert "author" in data, "ci_metadata.json missing 'author' field"
    assert isinstance(data["author"], str) and len(data["author"]) > 0, \
        "author must be a non-empty string"


def test_ci_metadata_has_email():
    with open("/home/user/ci_metadata.json") as f:
        data = json.load(f)
    assert "email" in data, "ci_metadata.json missing 'email' field"
    assert "@" in data["email"], f"email does not look like an email address: {data['email']}"


def test_ci_metadata_has_timestamp():
    with open("/home/user/ci_metadata.json") as f:
        data = json.load(f)
    assert "timestamp" in data, "ci_metadata.json missing 'timestamp' field"
    assert isinstance(data["timestamp"], str) and len(data["timestamp"]) > 0, \
        "timestamp must be a non-empty string"


def test_ci_metadata_has_description():
    with open("/home/user/ci_metadata.json") as f:
        data = json.load(f)
    assert "description" in data, "ci_metadata.json missing 'description' field"
    assert isinstance(data["description"], str) and len(data["description"]) > 0, \
        "description must be a non-empty string"


def test_ci_metadata_has_parents():
    with open("/home/user/ci_metadata.json") as f:
        data = json.load(f)
    assert "parents" in data, "ci_metadata.json missing 'parents' field"
    assert isinstance(data["parents"], list), "parents must be a JSON array"
    assert len(data["parents"]) >= 1, "parents array must have at least one element"


def test_ci_diff_stats_exists():
    assert os.path.isfile("/home/user/ci_diff_stats.txt"), \
        "/home/user/ci_diff_stats.txt does not exist."


def test_ci_diff_stats_not_empty():
    with open("/home/user/ci_diff_stats.txt") as f:
        content = f.read().strip()
    assert len(content) > 0, "/home/user/ci_diff_stats.txt is empty."


def test_ci_metadata_exported_bookmark_exists():
    result = run_jj(["bookmark", "list"])
    assert result.returncode == 0, f"jj bookmark list failed: {result.stderr}"
    assert "ci-metadata-exported" in result.stdout, \
        "Bookmark 'ci-metadata-exported' does not exist."

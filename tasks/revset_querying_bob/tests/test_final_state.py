import os
import subprocess

PROJECT_DIR = "/home/user/repo"

def test_user_config():
    result = subprocess.run(["jj", "config", "get", "user.name"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Bob" in result.stdout

def test_bob_feature_bookmark_exists():
    result = subprocess.run(["jj", "bookmark", "list"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0
    assert "bob-feature:" in result.stdout

def test_bob_txt_content():
    bob_txt_path = os.path.join(PROJECT_DIR, "bob.txt")
    assert os.path.isfile(bob_txt_path)
    with open(bob_txt_path) as f:
        content = f.read()
    assert "more work" in content

def test_commits_by_bob():
    # Query commits authored by Bob
    result = subprocess.run(["jj", "log", "-r", "author('Bob')", "-T", "description"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0
    assert "Bob's first commit" in result.stdout
    assert "Bob's second commit" in result.stdout

def test_revset_result():
    result_path = os.path.join(PROJECT_DIR, "bob_commits.txt")
    assert os.path.isfile(result_path), "bob_commits.txt does not exist."
    with open(result_path) as f:
        lines = [line.strip() for line in f if line.strip()]
    
    assert len(lines) == 2, f"Expected 2 Change IDs, got {len(lines)}."

    # Validate that these are indeed the Change IDs of Bob's commits
    for change_id in lines:
        result = subprocess.run(["jj", "log", "-r", change_id, "-T", "author.name() ++ '\n' ++ description"], cwd=PROJECT_DIR, capture_output=True, text=True)
        assert result.returncode == 0, f"Invalid Change ID: {change_id}"
        assert "Bob" in result.stdout, f"Commit {change_id} is not authored by Bob."
        assert "Bob's" in result.stdout, f"Commit {change_id} missing expected description."

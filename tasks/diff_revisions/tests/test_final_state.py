import os

PROJECT_DIR = "/home/user/myproject"
DIFF_FILE = os.path.join(PROJECT_DIR, "diff_output.txt")

def test_diff_file_exists():
    assert os.path.isfile(DIFF_FILE), "diff_output.txt should exist in the repository root."

def test_diff_content():
    with open(DIFF_FILE, "r") as f:
        content = f.read()

    # It should contain the expected git diff markers
    assert "diff --git" in content, "The diff should be in git format (missing 'diff --git')."
    assert "--- a/hello.txt" in content, "The diff should show the old file 'hello.txt'."
    assert "+++ b/hello.txt" in content, "The diff should show the new file 'hello.txt'."
    
    # It should show the exact lines changing
    assert "-Hello" in content, "The diff should show '-Hello' being removed."
    assert "+Hello World!" in content, "The diff should show '+Hello World!' being added."
    assert "+Hello World!!!" not in content, "The diff should not show the working copy changes."

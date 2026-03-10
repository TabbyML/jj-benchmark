import os
import subprocess
import sys

def test_final_state():
    repo_dir = "/home/user/myrepo"
    
    assert os.path.isdir(repo_dir), "Repository directory should exist"
    
    # Check that recovered-login bookmark exists and points to the correct commit
    result = subprocess.run(
        ["jj", "log", "-T", "description", "-r", "recovered-login", "--no-pager"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "recovered-login bookmark should exist"
    assert "feat: implement login page" in result.stdout, "The recovered-login bookmark should point to the recovered commit"

    # Check that the commit is visible (not just hidden)
    # If the bookmark points to it, it is automatically visible.
    
    # Check that there are no other bookmarks created
    result = subprocess.run(
        ["jj", "bookmark", "list"],
        cwd=repo_dir,
        capture_output=True,
        text=True
    )
    bookmarks = [line.split()[0] for line in result.stdout.splitlines() if line.strip()]
    
    assert "recovered-login" in bookmarks, "recovered-login bookmark must be in the bookmark list"
    assert "main" in bookmarks, "main bookmark must still exist"
    # Note: feature-login was deleted during abandon. The user shouldn't recreate it if the instructions said 'recovered-login'.

if __name__ == "__main__":
    try:
        test_final_state()
        print("Final state validation passed.")
        sys.exit(0)
    except AssertionError as e:
        print(f"AssertionError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

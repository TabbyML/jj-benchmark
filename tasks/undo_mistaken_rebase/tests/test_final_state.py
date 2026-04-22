import os, subprocess
def test_undo_rebase():
    res = subprocess.run(['jj', 'op', 'log'], cwd='/home/user/repo', capture_output=True, text=True)
    assert 'undo' in res.stdout.lower()

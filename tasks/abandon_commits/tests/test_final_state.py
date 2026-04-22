import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"

def run_jj_cmd(args):
    result = subprocess.run(["jj"] + args, cwd=PROJECT_DIR, capture_output=True, text=True)
    return result

def test_files_in_working_copy():
    assert os.path.isfile(os.path.join(PROJECT_DIR, "a.txt")), "a.txt should exist."
    assert os.path.isfile(os.path.join(PROJECT_DIR, "d.txt")), "d.txt should exist."
    assert not os.path.isfile(os.path.join(PROJECT_DIR, "b.txt")), "b.txt should be removed."
    assert not os.path.isfile(os.path.join(PROJECT_DIR, "c.txt")), "c.txt should be removed."

def test_experiment_bookmark_retained():
    res = run_jj_cmd(["log", "-r", "experiment", "-T", "description"])
    assert res.returncode == 0, "Bookmark 'experiment' should exist."
    assert "commit A" in res.stdout, "Bookmark 'experiment' should point to 'commit A'."

def test_draft_bookmark_deleted():
    res = run_jj_cmd(["log", "-r", "draft"])
    assert res.returncode != 0, "Bookmark 'draft' should be deleted and not resolvable."

def test_working_copy_description():
    res = run_jj_cmd(["log", "-r", "@", "-T", "description"])
    assert res.returncode == 0
    assert "cleanup complete" in res.stdout, "Working copy description should be 'cleanup complete'."

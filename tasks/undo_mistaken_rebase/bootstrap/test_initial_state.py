import os, shutil
PROJECT_DIR = '/home/user/repo'
def test_jj_binary_available():
    assert shutil.which('jj') is not None, 'jj binary not found in PATH.'
def test_repo_exists():
    assert os.path.isdir(PROJECT_DIR), f'Repo directory {PROJECT_DIR} does not exist.'
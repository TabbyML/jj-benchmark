import os
import subprocess

PROJECT_DIR = "/home/user/project"

def test_script_exists_and_executable():
    script_path = os.path.join(PROJECT_DIR, "show_commit.sh")
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_execution():
    script_path = os.path.join(PROJECT_DIR, "show_commit.sh")
    # Run the script with the revset argument
    result = subprocess.run(
        [script_path, "description(substring:\"Add configuration file\")"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    assert "diff --git a/config.txt b/config.txt" in result.stdout, "Script output does not contain Git-format diff."
    assert "+key=value" in result.stdout, "Script output does not contain the expected diff content."

def test_add_config_patch_exists_and_content():
    patch_path = os.path.join(PROJECT_DIR, "add_config.patch")
    assert os.path.isfile(patch_path), f"File {patch_path} does not exist."
    
    with open(patch_path, "r") as f:
        content = f.read()
        
    assert "diff --git a/config.txt b/config.txt" in content, "Patch file does not contain Git-format diff header."
    assert "+key=value" in content, "Patch file does not contain the expected addition."

def test_update_config_patch_exists_and_content():
    patch_path = os.path.join(PROJECT_DIR, "update_config.patch")
    assert os.path.isfile(patch_path), f"File {patch_path} does not exist."
    
    with open(patch_path, "r") as f:
        content = f.read()
        
    assert "diff --git a/config.txt b/config.txt" in content, "Patch file does not contain Git-format diff header."
    assert "-key=value" in content, "Patch file does not contain the expected removal."
    assert "+key=new_value" in content, "Patch file does not contain the expected addition."

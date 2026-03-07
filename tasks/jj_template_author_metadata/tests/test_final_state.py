import os
import subprocess
import pytest

REPO_DIR = "/home/user/repo"
CONFIG_FILE = os.path.join(REPO_DIR, ".jj/repo/config.toml")
LOG_OUTPUT_FILE = os.path.join(REPO_DIR, "formatted_log.txt")

def run_jj(args):
    return subprocess.run(["jj"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def test_alias_configured_correctly():
    assert os.path.isfile(CONFIG_FILE), f"Repo-specific config file {CONFIG_FILE} does not exist."
    
    with open(CONFIG_FILE, "r") as f:
        config_content = f.read()
    
    assert "mylog" in config_content, "The alias 'mylog' was not found in the repo-specific config.toml."
    
    result = run_jj(["config", "get", "aliases.mylog"])
    assert result.returncode == 0, f"Failed to get alias 'mylog' from config. Error: {result.stderr}"
    
    # We expect the alias to be mapped to the specific template array
    expected_substr1 = '"log"'
    expected_substr2 = '"-T"'
    expected_substr3 = 'commit_id.short(8) ++ "|" ++ author.name() ++ "|" ++ description.first_line() ++ "\\n"'
    
    # Handle possible escaping differences
    assert expected_substr1 in result.stdout and expected_substr2 in result.stdout, \
        f"Alias 'mylog' does not contain 'log' and '-T'. Got: {result.stdout}"
    
    assert "commit_id.short(8)" in result.stdout, "Template missing commit_id.short(8)"
    assert "author.name()" in result.stdout, "Template missing author.name()"
    assert "description.first_line()" in result.stdout, "Template missing description.first_line()"

def test_formatted_log_file_exists_and_correct():
    assert os.path.isfile(LOG_OUTPUT_FILE), f"Formatted log file {LOG_OUTPUT_FILE} does not exist."
    
    with open(LOG_OUTPUT_FILE, "r") as f:
        content = f.read()
        
    # We can run the command ourselves to see what the exact output should be
    expected_result = run_jj(["log", "-T", 'commit_id.short(8) ++ "|" ++ author.name() ++ "|" ++ description.first_line() ++ "\\n"'])
    assert expected_result.returncode == 0, f"Internal check failed: {expected_result.stderr}"
    
    expected_content = expected_result.stdout
    
    assert content.strip() == expected_content.strip(), \
        f"The content of {LOG_OUTPUT_FILE} does not match the expected template output.\nExpected:\n{expected_content}\nGot:\n{content}"

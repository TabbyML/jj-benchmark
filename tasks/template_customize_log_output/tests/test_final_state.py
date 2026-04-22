import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/repo"

def test_template_alias_configured():
    """Priority 1: Use jj CLI to verify the configured template alias."""
    result = subprocess.run(
        ["jj", "config", "get", "template-aliases.log_custom"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj config get' failed: {result.stderr}"
    
    output = result.stdout.strip()
    # The output might have quotes depending on how it was set, but it should contain the key parts
    assert "change_id.short()" in output, f"Alias missing change_id.short(): {output}"
    assert "description.first_line()" in output, f"Alias missing description.first_line(): {output}"
    assert "\" | \"" in output or "' | '" in output, f"Alias missing pipe separator: {output}"
    assert "\"\\n\"" in output or "'\\n'" in output, f"Alias missing newline: {output}"

def test_template_alias_output():
    """Priority 1: Use jj CLI to verify the output format using the alias."""
    # First, make a commit with a known description to test against
    subprocess.run(["jj", "describe", "-m", "Test commit description\nSecond line"], cwd=PROJECT_DIR, check=True)
    
    result = subprocess.run(
        ["jj", "log", "-T", "log_custom", "-r", "@", "--no-graph"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'jj log' failed: {result.stderr}"
    
    output = result.stdout.strip()
    # The output should look like "qpvz | Test commit description"
    parts = output.split(" | ")
    assert len(parts) == 2, f"Output format incorrect, expected 'ID | Description', got: {output}"
    
    change_id, description = parts
    assert len(change_id) > 0, "Change ID is empty"
    assert description == "Test commit description", f"Description incorrect, got: {description}"

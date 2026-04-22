import os

OUTPUT_FILE = "/home/user/root_path.txt"
EXPECTED_ROOT = "/home/user/repo"

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"The output file {OUTPUT_FILE} was not created."

def test_output_file_content():
    with open(OUTPUT_FILE, "r") as f:
        content = f.read().strip()
    
    assert content == EXPECTED_ROOT, f"Expected the file to contain exactly '{EXPECTED_ROOT}', but found '{content}'."

import os
import subprocess
import time
import socket
import pytest
import shutil
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/my-auth-app"

def wait_for_port(port, timeout=120):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module", autouse=True)
def start_app():
    if not os.path.exists(PROJECT_DIR):
        pytest.fail(f"Project directory {PROJECT_DIR} does not exist.")
    
    # Run migrations to ensure DB is up to date
    try:
        subprocess.run(["wasp", "db", "migrate-dev", "--name", "init"], cwd=PROJECT_DIR, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"wasp db migrate-dev failed: {e.stderr.decode()}")

    # Start the app
    process = subprocess.Popen(
        ["wasp", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for the app to be ready on port 3000
    if not wait_for_port(3000):
        import signal
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
        pytest.fail("Wasp app failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    import signal
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=30)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        pass

def test_main_wasp_content():
    main_wasp_path = os.path.join(PROJECT_DIR, "main.wasp")
    assert os.path.isfile(main_wasp_path), "main.wasp file is missing."
    with open(main_wasp_path, "r") as f:
        content = f.read()
    assert "fullName String" in content, "fullName field missing from User entity in main.wasp."
    assert "userSignupFields: import { userSignupFields } from \"@src/auth/signup.js\"" in content or "userSignupFields: import { userSignupFields } from \"@src/auth/signup\"" in content, "userSignupFields import missing from auth section in main.wasp."

def test_signup_logic_content():
    signup_js_path = os.path.join(PROJECT_DIR, "src", "auth", "signup.js")
    assert os.path.isfile(signup_js_path), "src/auth/signup.js file is missing."
    with open(signup_js_path, "r") as f:
        content = f.read()
    assert "defineUserSignupFields" in content, "defineUserSignupFields not used in src/auth/signup.js."
    assert "fullName:" in content, "fullName field logic missing from userSignupFields."

def test_signup_page_customization():
    signup_page_path = os.path.join(PROJECT_DIR, "src", "SignupPage.jsx")
    if not os.path.exists(signup_page_path):
        signup_page_path = os.path.join(PROJECT_DIR, "src", "SignupPage.tsx")
    
    assert os.path.isfile(signup_page_path), "SignupPage component file is missing."
    with open(signup_page_path, "r") as f:
        content = f.read()
    assert "additionalFields" in content, "additionalFields prop missing from SignupForm."
    assert "fullName" in content, "fullName field missing from additionalFields in SignupForm."

def test_main_page_display():
    main_page_path = os.path.join(PROJECT_DIR, "src", "MainPage.jsx")
    if not os.path.exists(main_page_path):
        main_page_path = os.path.join(PROJECT_DIR, "src", "MainPage.tsx")
    
    assert os.path.isfile(main_page_path), "MainPage component file is missing."
    with open(main_page_path, "r") as f:
        content = f.read()
    assert "user.fullName" in content or "{user.fullName}" in content, "fullName display missing from MainPage."

def test_browser_verification():
    reason = "The application should feature a customized signup form with a 'Full Name' field and display it after login."
    truth = (
        "Navigate to http://localhost:3000/signup. Verify that an input field with the label 'Full Name' exists in the form. "
        "Try to sign up without entering a Full Name and verify the error 'Full name is required'. "
        "Fill in the form with Username: 'testuser', Password: 'password123', Full Name: 'John Doe', and submit. "
        "Verify redirection to the main page and that 'Hello, John Doe!' is displayed."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/custom_auth_fields"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"

def test_database_persistence():
    # Attempt to find the SQLite database file
    db_path = os.path.join(PROJECT_DIR, ".wasp", "out", "db", "dev.db")
    if not os.path.exists(db_path):
        # Alternative common Wasp DB locations
        db_path = os.path.join(PROJECT_DIR, "dev.db")
    
    if os.path.exists(db_path):
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            # Check for the user and fullName
            cursor.execute("SELECT fullName FROM User WHERE username = 'testuser'")
            row = cursor.fetchone()
            assert row is not None, "testuser was not found in the database User table."
            assert row[0] == "John Doe", f"Expected fullName 'John Doe' for testuser, but got '{row[0]}'."
        except sqlite3.OperationalError as e:
            # Table might not exist or field might be missing
            pytest.fail(f"Database query failed: {e}")
        finally:
            conn.close()
    else:
        # If DB file is not found, we rely on the browser check
        pass

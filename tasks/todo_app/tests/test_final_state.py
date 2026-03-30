import os
import subprocess
import time
import socket
import pytest
import signal
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/todo-app"

def wait_for_port(port, timeout=150):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the app
    process = subprocess.Popen(
        ["wasp", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for the app to be ready
    if not wait_for_port(3000):
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
        pytest.fail("Wasp app failed to start on port 3000 within timeout.")
    
    yield
    
    # Shut down
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=30)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        pass

def test_files_exist():
    required_files = [
        "main.wasp",
        "schema.prisma",
        "src/queries.ts",
        "src/actions.ts",
        "src/MainPage.tsx"
    ]
    for f in required_files:
        path = os.path.join(PROJECT_DIR, f)
        assert os.path.isfile(path), f"Required file {path} is missing."

def test_schema_definitions():
    schema_path = os.path.join(PROJECT_DIR, "schema.prisma")
    with open(schema_path, "r") as f:
        content = f.read()
    assert "model User" in content, "User model missing in schema.prisma"
    assert "model Task" in content, "Task model missing in schema.prisma"
    assert "description" in content and "String" in content, "Task.description field missing"
    assert "isDone" in content and "Boolean" in content, "Task.isDone field missing"

def test_main_wasp_config():
    wasp_path = os.path.join(PROJECT_DIR, "main.wasp")
    with open(wasp_path, "r") as f:
        content = f.read()
    assert "auth:" in content, "Auth configuration missing in main.wasp"
    assert "usernameAndPassword:" in content, "usernameAndPassword auth method missing"
    assert "query getTasks" in content, "getTasks query missing"
    assert "action createTask" in content, "createTask action missing"
    assert "action updateTask" in content, "updateTask action missing"
    assert "authRequired: true" in content, "MainPage should require authentication"

def test_operation_security():
    queries_path = os.path.join(PROJECT_DIR, "src/queries.ts")
    with open(queries_path, "r") as f:
        content = f.read()
    assert "context.user" in content, "Security check (context.user) missing in queries.ts"

    actions_path = os.path.join(PROJECT_DIR, "src/actions.ts")
    with open(actions_path, "r") as f:
        content = f.read()
    assert "context.user" in content, "Security check (context.user) missing in actions.ts"

def test_browser_verification(start_app):
    reason = "The Wasp Todo application should support multi-user authentication, task creation, and task toggling with data isolation."
    truth = (
        "1. Navigate to http://localhost:3000/signup. Create an account with username 'testuser' and password 'password123'. "
        "2. Navigate to http://localhost:3000/login. Login with the credentials created above. "
        "3. On the main page, enter 'Buy milk' in the task description field and click 'Create task'. "
        "4. Refresh the page. Verify that the task 'Buy milk' is still visible. "
        "5. Click the checkbox next to 'Buy milk'. Verify that the state updates. "
        "6. Logout and signup with a different user 'otheruser' and password 'password123'. "
        "7. Verify that the task 'Buy milk' is NOT visible for 'otheruser'. "
        "8. Click the 'Logout' button. Verify redirection to the login page."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_verification"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"

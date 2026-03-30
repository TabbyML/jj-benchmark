import os
import subprocess
import time
import socket
import pytest
import sqlite3
import signal
from pathlib import Path
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/team_manager"

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
    # Start the app
    process = subprocess.Popen(
        ["wasp", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for the app to be ready
    # Client on 3000, Server on 3001
    if not wait_for_port(3000) or not wait_for_port(3001):
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except Exception:
            pass
        pytest.fail("Wasp app failed to start and listen on required ports (3000, 3001).")
    
    yield
    
    # Shut down the app
    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=30)
    except Exception:
        pass

def test_project_structure():
    assert os.path.isdir(PROJECT_DIR), "Project directory /home/user/team_manager not found."
    assert os.path.isfile(os.path.join(PROJECT_DIR, "main.wasp")), "main.wasp not found in project directory."
    assert os.path.isfile(os.path.join(PROJECT_DIR, "schema.prisma")), "schema.prisma not found in project directory."

def test_schema_content():
    schema_path = os.path.join(PROJECT_DIR, "schema.prisma")
    with open(schema_path) as f:
        content = f.read()
    assert "model User" in content, "User model missing from schema.prisma."
    assert "model Team" in content, "Team model missing from schema.prisma."
    assert "model Task" in content, "Task model missing from schema.prisma."
    assert "fullName" in content, "fullName field missing from User model in schema.prisma."

def test_auth_configuration():
    wasp_path = os.path.join(PROJECT_DIR, "main.wasp")
    with open(wasp_path) as f:
        content = f.read()
    assert "userSignupFields" in content, "userSignupFields not configured in main.wasp."
    assert "usernameAndPassword" in content, "usernameAndPassword auth method missing from main.wasp."

def test_browser_workflow():
    reason = "Verify the collaborative task manager: signup with fullName, team creation, task creation, and role-based access control."
    truth = (
        "1. Navigate to http://localhost:3000/signup. "
        "2. Sign up as Alice (username: 'alice', password: 'password123', fullName: 'Alice Smith'). "
        "3. Log in as Alice. "
        "4. Create a new team named 'Alpha Team'. "
        "5. Within 'Alpha Team', create a task with description 'Alice's Task'. "
        "6. Verify that 'Alice's Task' is visible in the team detail page. "
        "7. Log out and sign up as Bob (username: 'bob', password: 'password123', fullName: 'Bob Jones'). "
        "8. Attempt to access the 'Alpha Team' page or its tasks and verify that access is denied (403 Forbidden)."
    )
    
    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_workflow"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"

def test_database_integrity():
    # Find the SQLite database
    db_path = os.path.join(PROJECT_DIR, ".wasp/out/db/dev.db")
    if not os.path.exists(db_path):
        db_files = list(Path(PROJECT_DIR).rglob("dev.db"))
        if db_files:
            db_path = str(db_files[0])
        else:
            pytest.fail("SQLite database file (dev.db) not found.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verify Alice's fullName in DB
        cursor.execute("SELECT fullName FROM User WHERE username = 'alice'")
        row = cursor.fetchone()
        assert row is not None, "User 'alice' not found in database."
        assert row[0] == "Alice Smith", f"Expected fullName 'Alice Smith', found '{row[0]}'."
        
        # Verify Team creation
        cursor.execute("SELECT id FROM Team WHERE name = 'Alpha Team'")
        team_row = cursor.fetchone()
        assert team_row is not None, "Team 'Alpha Team' not found in database."
        team_id = team_row[0]
        
        # Verify Task creation
        cursor.execute("SELECT COUNT(*) FROM Task WHERE teamId = ?", (team_id,))
        task_count = cursor.fetchone()[0]
        assert task_count > 0, "No tasks found for 'Alpha Team' in database."
        
        # Verify Cascade Delete
        cursor.execute("DELETE FROM Team WHERE id = ?", (team_id,))
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM Task WHERE teamId = ?", (team_id,))
        task_count_after = cursor.fetchone()[0]
        assert task_count_after == 0, "Cascade delete failed: Tasks still exist after Team deletion."
        
    finally:
        conn.close()

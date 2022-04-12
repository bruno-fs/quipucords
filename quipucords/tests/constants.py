"""Test contants."""
from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).absolute().parent.parent.parent

POSTGRES_DB = "qpc-db"
POSTGRES_PASSWORD = "qpc"
POSTGRES_USER = "qpc"
QPC_COMMIT = "test-commit"
QPC_SERVER_PASSWORD = "test-password"
QPC_SERVER_USERNAME = "test-username"
SCAN_TARGET_USERNAME = "container-user"
SCAN_TARGET_PASSWORD = "password"

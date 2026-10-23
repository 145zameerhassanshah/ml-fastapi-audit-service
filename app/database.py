import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "audit.db"

def get_db_path() -> str:
    return os.getenv("AUDIT_DB_PATH", str(DEFAULT_DB_PATH))

@contextmanager
def get_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_database() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS prediction_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp_utc TEXT NOT NULL,
                status TEXT NOT NULL,
                request_payload TEXT,
                predicted_class INTEGER,
                probability_class_1 REAL,
                error_message TEXT,
                model_version TEXT
            )
        """)

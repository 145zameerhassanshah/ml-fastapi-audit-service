import json
from datetime import datetime, timezone
from typing import Any
from app.database import get_connection

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def log_request(*, status: str, request_payload: Any = None, predicted_class: int | None = None, probability_class_1: float | None = None, error_message: str | None = None, model_version: str | None = None) -> None:
    payload_text = request_payload if isinstance(request_payload, str) else json.dumps(request_payload, ensure_ascii=False)
    with get_connection() as conn:
        conn.execute("""INSERT INTO prediction_logs (timestamp_utc,status,request_payload,predicted_class,probability_class_1,error_message,model_version) VALUES (?,?,?,?,?,?,?)""", (utc_now_iso(), status, payload_text, predicted_class, probability_class_1, error_message, model_version))

def fetch_recent_logs(limit: int = 20) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM prediction_logs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in rows]

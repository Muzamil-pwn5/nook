from datetime import datetime, timezone
from pathlib import Path
import json


LOG_FILE = Path(__file__).resolve().parents[3] / "audit.log"


def record_audit_event(
    *,
    tool_name: str,
    arguments: dict,
    success: bool,
    result: dict | None = None,
    error: str | None = None,
    approved: bool = False,
) -> None:
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool_name": tool_name,
        "arguments": arguments,
        "approved": approved,
        "success": success,
        "result": result,
        "error": error,
    }

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, default=str) + "\n")
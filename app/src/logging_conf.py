import logging
import json
from datetime import datetime, timezone

class jsonFormatter(logging.Formatter):
    def format(self, record) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat() + "z",
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None),
            "endpoint": getattr(record, "endpoint", None),
            "latency": getattr(record, "latency", None),
            "error_message": getattr(record, "error_message", None),
        }
        return json.dumps(payload, default=str)

logger = logging.getLogger("app")
handler = logging.StreamHandler()
handler.setFormatter(jsonFormatter())
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False
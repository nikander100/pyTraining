import logging, pathlib
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone
from pythonjsonlogger.json import JsonFormatter 

formatter = JsonFormatter(
    fmt="%(timestamp)s %(levelname)s %(message)s %(request_id)s %(endpoint)s %(status_code)s %(latency)s %(error_message)s %(client_ip)s %(user_agent)s"
)

class DefaultFilter(logging.Filter):
    def filter(self, record) -> bool:
        record.timestamp = getattr(
            record,
            "timestamp",
            datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        )
        record.request_id = getattr(record, "request_id", None)
        record.endpoint = getattr(record, "endpoint", None)
        record.status_code = getattr(record, "status_code", None)
        record.latency = getattr(record, "latency", None)
        record.error_message = getattr(record, "error_message", None)
        record.client_ip = getattr(record, "client_ip", None)
        record.user_agent = getattr(record, "user_agent", None)
        return True

logger = logging.getLogger("app")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.addFilter(DefaultFilter())

log_dir = pathlib.Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)

file_handler = RotatingFileHandler(
    filename=log_dir / "app.log",
    maxBytes=5_000_000,
    backupCount=3,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)
file_handler.addFilter(DefaultFilter())

logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(file_handler)
logger.propagate = False
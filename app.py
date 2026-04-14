import json
import time
import logging
import sys
import os
import random
from datetime import datetime, timezone

# Configure root logger to output to STDOUT only — no file handlers
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# Custom JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": "hello-world-app",
            "message": record.getMessage(),
            "logger": record.name,
            "pid": os.getpid(),
        }
        # Attach extra fields if any
        if hasattr(record, "extra"):
            log_entry.update(record.extra)
        return json.dumps(log_entry)

handler.setFormatter(JsonFormatter())
logger = logging.getLogger("hello-world")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
# Prevent propagation to avoid duplicate logs
logger.propagate = False

MESSAGES = [
    ("INFO",  "Hello, World! Everything is running fine."),
    ("INFO",  "Heartbeat OK — container is alive."),
    ("DEBUG", "Processing cycle complete. No anomalies detected."),
    ("WARNING", "Simulated warning: memory usage slightly elevated."),
    ("ERROR", "Simulated error: transient upstream timeout (non-fatal)."),
]

def emit_log():
    level, msg = random.choice(MESSAGES)
    extra = {
        "iteration": emit_log.counter,
        "uptime_seconds": round(time.time() - emit_log.start_time, 2),
        "random_value": random.randint(1, 100),
    }
    record = logging.LogRecord(
        name="hello-world",
        level=getattr(logging, level),
        pathname=__file__,
        lineno=0,
        msg=msg,
        args=(),
        exc_info=None,
    )
    record.extra = extra
    logger.handle(record)
    emit_log.counter += 1

emit_log.counter = 0
emit_log.start_time = time.time()

if __name__ == "__main__":
    logger.info("Application started", extra={})
    while True:
        emit_log()
        time.sleep(3)

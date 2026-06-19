import json
import logging
from datetime import datetime


class JsonFormatter(logging.Formatter):

    def format(self, record):

        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": getattr(
                record,
                "request_id",
                "N/A"
            )
        }

        return json.dumps(log_record)


def setup_logging():

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    root_logger.handlers.clear()
    root_logger.addHandler(handler)
from dataclasses import dataclass
from datetime import datetime

from streamstats.errors import InvalidLogError, InvalidTimestampError


@dataclass
class Log:
    timestamp: datetime
    level: str
    source: str
    message: str


def validateLog(timestamp,level,source):
    if level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise InvalidLogError("Invalid log level")
    if len(source) == 0:
        raise InvalidLogError("Empty source")

    try:
        timestamp = datetime.fromisoformat(timestamp)
    except ValueError as e:
        raise InvalidTimestampError("Invalid timestamp")

    return timestamp
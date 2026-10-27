from dataclasses import dataclass
from datetime import datetime

@dataclass
class Log:
    timestamp: datetime
    level: str
    source: str
    message: str



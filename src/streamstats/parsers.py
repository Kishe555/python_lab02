from datetime import datetime
from os import SEEK_SET, SEEK_END
from models import Log
from src.streamstats.errors import InvalidTimestampError, InvalidLogError, StreamStatsError
import json

from src.streamstats.models import validateLog


class CSVIterator:
    def __init__(self, filename: str):
        self.fp = open(filename, "r", encoding="UTF-8")
        self.fp.seek(0, SEEK_END)
        self.pos_end = self.fp.tell()
        self.fp.seek(0, SEEK_SET)
        line = self.fp.readline().replace("\r","").replace("\n","")
        if line != "timestamp,level,source,message":
            self.fp.seek(0, SEEK_SET)

    def __iter__(self):
        return self

    def __next__(self):
        if self.fp.tell() == self.pos_end:
            raise StopIteration
        line = self.fp.readline().replace("\r","").replace("\n","").split(',')
        if len(line) != 4:
            raise InvalidLogError("Not enough fields")
        timestamp, level, source, message = line

        try:
            timestamp = validateLog(timestamp, level, source)
        except StreamStatsError as e:
            raise e
        variable = Log(timestamp= timestamp,
                      level= level,
                      source= source,
                      message= message )
        return variable

class JSONLIterator:
    def __init__(self, filename: str):
        self.fp = open(filename, "r", encoding="UTF-8")
        self.fp.seek(0, SEEK_END)
        self.pos_end = self.fp.tell()
        self.fp.seek(0, SEEK_SET)

    def __iter__(self):
        return self

    def __next__(self):
        if self.fp.tell() == self.pos_end:
            raise StopIteration
        line = self.fp.readline().replace("\r", "").replace("\n", "")

        try:
            data = json.loads(line)
        except ValueError as e:
            print(line)
            raise InvalidLogError("Invalid line in JSONL")
        if "timestamp" not in data:
            raise InvalidLogError("Timestamp missing")
        if "level" not in data:
            raise InvalidLogError("Level missing")
        if "source" not in data:
            raise InvalidLogError("Source missing")
        if "message" not in data:
            raise InvalidLogError("Message missing")

        try:
            timestamp = validateLog(data["timestamp"], data["level"], data["source"])
        except StreamStatsError as e:
            raise e

        variable = Log(timestamp = timestamp,
                    level = data["level"],
                    source = data["source"],
                    message = data["message"])
        return variable
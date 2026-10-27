from datetime import datetime
from os import SEEK_SET, SEEK_END
from models import Log
from src.streamstats.errors import InvalidTimestampError, InvalidLogError


class MyIter:
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
        if level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise InvalidLogError("Invalid log level")
        if len(source) == 0:
            raise InvalidLogError("Empty source")
        try:
            timestamp = datetime.fromisoformat(timestamp)
        except ValueError as e:
            raise InvalidTimestampError("Invalid timestamp")
        variable = Log(timestamp= timestamp,
                      level= level,
                      source= source,
                      message= message )
        return variable


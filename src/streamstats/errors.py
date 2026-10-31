class StreamStatsError(Exception):
    pass

class InvalidLogError(StreamStatsError):
    pass

class InvalidTimestampError(StreamStatsError):
    pass

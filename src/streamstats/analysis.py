from typing import Any
from streamstats.models import Log
from datetime import datetime


ERROR_LEVELS = {"ERROR", "CRITICAL"}

def sort_key(item: tuple[str, int]) -> tuple[int, str]:
    source, count = item
    return -count, source

def top_error_sources(events) -> list[tuple[str,int]]:
    sources = counter(events, key=lambda elm: elm.source, cmp = lambda elm: elm.level in ERROR_LEVELS)

    return sorted(sources.items(), key=sort_key)[:5]

def time_range(events) -> tuple[datetime, datetime]:
    times = [event.timestamp for event in events]
    return min(times), max(times)


def counter(events, key = lambda x: 0, cmp= lambda x: True):
    stat = {}
    for event in events:
        if cmp(event):
            stat[key(event)] = stat.get(key(event), 0) + 1

    return stat

def counter_all(events):
    return counter(events)[0]

def counter_levels(events):
    return counter(events, key=lambda elm: elm.level)


def counter_sources(events):
    return counter(events, key=lambda elm: elm.source)


def get_events(files, iterator_class):
    for filename in files:
        reader = iterator_class(filename)

        try:
            yield from reader
        finally:
            reader.fp.close()
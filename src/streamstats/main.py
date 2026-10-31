from src.streamstats.parsers import CSVIterator,  JSONLIterator
from src.streamstats.analysis import top_error_sources, time_range, counter_sources, counter_levels, counter_all
import json
import argparse

# for source, count in top_error_sources(MyIter("../data.csv")):
#     print(f"{source}: {count}")
#
# for times in time_range(MyIter("../data.csv")):
#     print(times)
#
# for event,count in counter_sources(MyIter("../data.csv")).items():
#     print(f"{event}: {count}")
# for level,count in counter_levels(MyIter("../data.csv")).items():
#     print(f"{level}: {count}")
# print(counter_all(MyIter("../data.csv")))
report = {}



top5error = {}
for source, count in top_error_sources(JSONLIterator("../data.jsonl")):
     top5error[source] = count
report["top 5 sources of error"] = top5error

time_min, time_max = time_range(JSONLIterator("../data.jsonl"))
report["first timestamp"] = str(time_min)
report["last timestamp"] = str(time_max)

report["total amount of events"] = counter_all(JSONLIterator("../data.jsonl"))

report["amount of events by level"] = counter_levels(JSONLIterator("../data.jsonl"))
report["amount of events by sources"] = counter_sources(JSONLIterator("../data.jsonl"))

json.dump(report, open("report.json", "w", encoding="utf-8"), indent = 4)


def main() -> float:
     parser = argparse.ArgumentParser("анализатор")

     commands = parser.add_subparsers(dest="command", required=True)

     analyzer_parser = commands.add_parser("analyze")
     analyzer_parser.add_argument("input", narg="+")

     analyzer_parser.add_argument("--format",  required=True, choices=["csv", "jsonl"])
     analyzer_parser.add_argument("--output",  required=True)
     analyzer_parser.add_argument("--skip-invalid", action="store_true")
     args = parser.parse_args()



if __name__ == "__main__":
    main()
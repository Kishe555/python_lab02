from streamstats.parsers import CSVIterator,  JSONLIterator
from streamstats.analysis import top_error_sources, time_range, counter_sources, counter_levels, counter_all, \
     get_events
import json
import argparse

#python -m streamstats analyze data.csv --format csv --output report777.json

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

# report = {}
#
#
#
# top5error = {}
# for source, count in top_error_sources(JSONLIterator("../data.jsonl")):
#      top5error[source] = count
# report["top 5 sources of error"] = top5error
#
# time_min, time_max = time_range(JSONLIterator("../data.jsonl"))
# report["first timestamp"] = str(time_min)
# report["last timestamp"] = str(time_max)
#
# report["total amount of events"] = counter_all(JSONLIterator("../data.jsonl"))
#
# report["amount of events by level"] = counter_levels(JSONLIterator("../data.jsonl"))
# report["amount of events by sources"] = counter_sources(JSONLIterator("../data.jsonl"))
#
# json.dump(report, open("report.json", "w", encoding="utf-8"), indent = 4)

def reporter(files, iterator_class, report_file):
     time_min, time_max = time_range(get_events(files, iterator_class))
     total_amount_of_events = counter_all(get_events(files, iterator_class))
     amount_of_events_by_level = counter_levels(get_events(files, iterator_class))
     amount_of_events_by_sources = counter_sources(get_events(files, iterator_class))

     top5error = {}
     for source, count in top_error_sources(get_events(files, iterator_class)):
          top5error[source] = count

     report = {"top 5 sources of error": top5error,
               "first timestamp": str(time_min),
               "last timestamp": str(time_max),
               "total amount of events": total_amount_of_events,
               "amount of events by level": amount_of_events_by_level,
               "amount of events by sources": amount_of_events_by_sources}

     json.dump(report, open(report_file, "w", encoding="utf-8"), indent = 4)





def main() -> None:
     parser = argparse.ArgumentParser("анализатор")

     commands = parser.add_subparsers(dest="command", required=True)

     analyzer_parser = commands.add_parser("analyze")
     analyzer_parser.add_argument("input", nargs="+")

     analyzer_parser.add_argument("--format",  required=True, choices=["csv", "jsonl"])
     analyzer_parser.add_argument("--output",  required=True)
     analyzer_parser.add_argument("--skip-invalid", action="store_true")
     args = parser.parse_args()

     iterator_class = (CSVIterator if args.format == "csv" else JSONLIterator)

     reporter(args.input ,iterator_class, args.output)

if __name__ == "__main__":
    main()
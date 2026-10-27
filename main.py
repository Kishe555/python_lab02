from src.streamstats.parsers import MyIter
from src.streamstats.analysis import top_error_sources, time_range, counter_sources, counter_levels, counter_all
import json

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
for source, count in top_error_sources(MyIter("../data.csv")):
     top5error[source] = count
report["top 5 sources of error"] = top5error

time_min, time_max = time_range(MyIter("../data.csv"))
report["first timestamp"] = str(time_min)
report["last timestamp"] = str(time_max)

report["total amount of events"] = counter_all(MyIter("../data.csv"))

report["amount of events by level"] = counter_levels(MyIter("../data.csv"))
report["amount of events by sources"] = counter_sources(MyIter("../data.csv"))

json.dump(report, open("report.json", "w", encoding= "utf-8"), indent = 4 )

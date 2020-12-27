from time_tracker import *
import sys

time_tracker = TimeTracker()

try:
    time_tracker.initialize_me()
except json.decoder.JSONDecodeError:
    print("\nFailed to load data from ./TimeTrackerData.json")


from time_tracker import *
import sys

DAYS_TO_LOAD = 7

def initialize_time_trackers():
    time_trackers = []
    for i in range(DAYS_TO_LOAD):
        time_tracker = TimeTracker(i)
        try:
            time_tracker.initialize_me()
            time_trackers.append(time_tracker)
        except IOError as e:
            print(e)
            pass

    return time_trackers


time_trackers = initialize_time_trackers()
print(time_trackers)

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


def update_categories_in_time_trackers():
    for time_tracker in time_trackers:
        time_tracker.update_all_activities_categories()
        time_tracker.update_all_categories_time_spend()


def save_data():
    for time_tracker in time_trackers:
        time_tracker.save_me()


def update_data():
    update_categories_in_time_trackers()
    save_data()
    print("INFO: Data updated")


time_trackers = initialize_time_trackers()
update_data()

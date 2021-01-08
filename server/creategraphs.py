from time_tracker import *
import sys

def initialize_time_trackers(days_to_load):
    time_trackers = []
    for i in range(days_to_load):
        time_tracker = TimeTracker(i)
        try:
            time_tracker.initialize_me()
            time_trackers.append(time_tracker)
        except IOError as e:
            print(e)
            pass
    return time_trackers


def initialize_categories():
    ttCategories = TimeTrackerCategories()
    ttCategories.initialize_me()
    return ttCategories

def create_graphs_for_time_trackers(time_trackers):
    for time_tracker in time_trackers:
        time_tracker.create_graph()


def create_legend(time_trackers):
    time_trackers[0].create_graph(create_legend_png=True)


def main():
    print("INFO: Trying to create new graphs")
    time_tracker_categories_obj = initialize_categories()
    time_trackers = initialize_time_trackers(int(sys.argv[1]))
    if len(time_trackers):
        create_graphs_for_time_trackers(time_trackers)
        create_legend(time_trackers)
    print("INFO: Created new graphs")

if __name__ == "__main__":
    try:
        main()
    except:
        print("ERROR: Failed to create new graphs")
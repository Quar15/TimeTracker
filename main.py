import pygetwindow as gw
from time_tracker import *
import sys
import time

def get_active_window():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        _active_window_name = gw.getActiveWindow().title
    
    else:
        print("sys.platform={platform} is not supported.".format(platform=sys.platform))

    return _active_window_name


def set_time_spend(_active_window_name, time_spend):

    curr_activity = time_tracker.search_for_activity(_active_window_name, time_spend)

    if curr_activity == None:
        curr_activity = Activity(_active_window_name, [], time_spend)
        time_tracker.add_activity(curr_activity)

    return curr_activity


def update_timer():
    curr_activity_timer.update_time_spend()
    return curr_activity_timer.time_spend


def update_activity_categories(activity):
    for category in time_tracker.categories:
        for keyword in category.keywords:
            if keyword in activity.name and category.id not in activity.categories_id:
                activity.add_category(category.id)


def create_category(name, wage, keywords):
    new_category = ActivityCategory(len(time_tracker.categories), name, wage, 0, keywords)
    if time_tracker.search_category_by_name(new_category.name) == None: # @TODO: Create categories comparator
        time_tracker.add_category(new_category)
        time_tracker.update_all_activities_categories()


active_window_name = get_active_window()
activity_name = ""
time_tracker = TimeTracker()
curr_activity_timer = Timer()
opened_activities_names = []

try:
    time_tracker.initialize_me()
except json.decoder.JSONDecodeError:
    print("\nFailed to load data from ./TimeTrackerData.json")


create_category("Web", 1, ["Mozilla Firefox", "Google Chrome"])
create_category("Coding", 2, ["Visual Studio", "Stack Overflow"])

try:
    while True:
        new_window_name = get_active_window()

        if active_window_name != new_window_name and new_window_name != "" and active_window_name != "":
            print(active_window_name)
            
            time_spend = update_timer()
            curr_activity = set_time_spend(active_window_name, time_spend)

            if curr_activity.name not in opened_activities_names:
                update_activity_categories(curr_activity)
                opened_activities_names.append(curr_activity.name)
            
            active_window_name = new_window_name
        
        time.sleep(1)

except KeyboardInterrupt:
    print(opened_activities_names)
    set_time_spend(active_window_name, update_timer())
    time_tracker.save_me()
    print("\nData saved! Have a nice day!")
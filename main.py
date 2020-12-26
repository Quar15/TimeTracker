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


active_window_name = get_active_window()
activity_name = ""
time_tracker = TimeTracker()
curr_activity_timer = Timer()


try:
    time_tracker.initialize_me()
except json.decoder.JSONDecodeError:
    print("\nFailed to load data from ./TimeTrackerData.json")


try:
    while True:
        new_window_name = get_active_window()

        if active_window_name != new_window_name and new_window_name != "" and active_window_name != "":
            print(active_window_name)
            
            curr_activity_timer.update_time_spend()
            time_spend = curr_activity_timer.time_spend
            set_time_spend(active_window_name, time_spend)                
            
            active_window_name = new_window_name
        
        time.sleep(1)

except KeyboardInterrupt:
    curr_activity_timer.update_time_spend()
    set_time_spend(active_window_name, curr_activity_timer.time_spend)
    time_tracker.save_me()
    print("\nData saved! Have a nice day!")
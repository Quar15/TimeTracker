import pygetwindow as gw
from time_tracker import *
import sys
import time
import requests

SERVER_IP = "127.0.0.1"
SERVER_PORT = "5000"


def get_active_window():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        try:
            _active_window_name = gw.getActiveWindow().title
        except AttributeError:
            print("WARNING: No active window found")
            _active_window_name = ""
    
    else:
        print("sys.platform={platform} is not supported.".format(platform=sys.platform))

    return _active_window_name


def set_time_spend(_active_window_name, time_spend):

    curr_activity = time_tracker.search_for_activity(_active_window_name, time_spend)

    if curr_activity == None:
        curr_activity = Activity(_active_window_name, time_spend)
        time_tracker.add_activity(curr_activity)

    return curr_activity


def update_timer():
    curr_activity_timer.update_time_spend()
    return curr_activity_timer.time_spend


def send_data():
    try:
        url = "http://" + SERVER_IP + ":" + SERVER_PORT + "/send-data"
        with open(time_tracker.file_name, "r") as f:
                data = json.load(f)
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print("INFO: Data saved on server")
    except:
        print("ERROR: Sending data to server failed")


active_window_name = get_active_window()
activity_name = ""
time_tracker = TimeTracker()
curr_activity_timer = Timer()
opened_activities_names = []

try:
    time_tracker.initialize_me()
except json.decoder.JSONDecodeError:
    print("\nFailed to load data from ./TimeTrackerData.json")


try:
    while True:
        new_window_name = get_active_window()

        if active_window_name != new_window_name and new_window_name != "" and active_window_name != "":
            print(active_window_name)
            
            time_spend = update_timer()
            curr_activity = set_time_spend(active_window_name, time_spend)
            
            active_window_name = new_window_name
        
        time.sleep(1)

except KeyboardInterrupt:
    set_time_spend(active_window_name, update_timer())
    time_tracker.save_me()
    send_data()
    print("\nData saved! Have a nice day!")
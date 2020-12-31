import json
import os
from datetime import datetime


class TimeTracker:

    def __init__(self):
        self.activities = []
        self.date = datetime.today().strftime("%d%m%Y")
        self.file_name = "./data/TimeTrackerData" + self.date + ".json"

    def initialize_me(self):
        if os.path.isfile(self.file_name):
            with open(self.file_name, "r") as f:
                data = json.load(f)
                self.activities = self.get_activities_from_json(data)
        else:

            print("Welcome to Time Tracker!")

    def get_activities_from_json(self, data):
        activity_list = []
        for activity in data['activities']:
            activity_list.append(
                Activity(activity['name'], activity['total_time_spend'])
            )
        return activity_list

    def add_activity(self, new_activity):
        self.activities.append(new_activity)

    def search_for_activity(self, searched_activity_window_name, time_spend):
        for activity in self.activities:
            if activity.name == searched_activity_window_name:
                activity.total_time_spend += time_spend
                return activity
        return None

    def serialize_list_to_json(self, list_to_serialize):
        object_list = []
        for obj in list_to_serialize:
            object_list.append(obj.serialize())
        return object_list

    def save_to_json(self, path, serialized_data):
        with open(path, "w") as f:
            json.dump(serialized_data, f, indent=4, sort_keys=True)

    def save_me(self):
        self.save_to_json(self.file_name, {"activities": self.serialize_list_to_json(self.activities)})


class Activity:
    
    def __init__(self, _name, _total_time_spend=0):
        self.name = _name
        self.total_time_spend = _total_time_spend

    def serialize(self):
        return {
            "name": self.name,
            "categories_id": [],
            "total_time_spend" : int(self.total_time_spend)
        }


class Timer:

    def __init__(self):
        self.time_spend = 0
        self.start_tic = datetime.now()
        self.end_tic = 0
    
    def update_time_spend(self):
        self.end_tic = datetime.now()
        dt_time_spend = self.end_tic - self.start_tic
        self.time_spend = dt_time_spend.total_seconds()
        self.start_tic = self.end_tic
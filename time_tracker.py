import json
import os
from datetime import datetime


class TimeTracker:

    def __init__(self):
        self.activities = []

    def initialize_me(self):
        if os.path.isfile("./TimeTrackerData.json"):
            with open("./TimeTrackerData.json", "r") as f:
                data = json.load(f)
                self.activities = self.get_activities_from_json(data)
        else:
            print("Welcome to Time Tracker!")

    def get_activities_from_json(self, data):
        activity_list = []
        for activity in data['activities']:
            activity_list.append(
                Activity(activity['name'], activity['categories'], activity['total_time_spend'])
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

    def serialize(self):
        return {
            "activities": self.serialize_activities_to_json()
        }

    def serialize_activities_to_json(self):
        activities_list = []
        for activity in self.activities:
            activities_list.append(activity.serialize())
        return activities_list

    def save_me(self):
        with open("./TimeTrackerData.json", "w") as f:
            json.dump(self.serialize(), f, indent=4, sort_keys=True)


class ActivityCategory:
    def __init__(self, _name, _value, _total_time_spend=0):
        self.name = _name
        self.value = _value
        self.total_time_spend = _total_time_spend

    def update_total_time_spend(self, activities):
        for activity in activities:
            if(self in activity.categories):
                self.total_time_spend += activity.total_time_spend

    def serialize(self):
        return {
            "name": self.name,
            "value": self.value
        }


class Activity:
    
    def __init__(self, _name, _categories, _total_time_spend=0):
        self.name = _name
        self.categories = _categories
        self.total_time_spend = _total_time_spend

    def serialize(self):
        return {
            "name": self.name,
            "categories": self.serialize_categories_to_json(),
            "total_time_spend" : self.total_time_spend
        }

    def serialize_categories_to_json(self):
        categories_list = []
        for category in self.categories:
            categories_list.append(category.serialize())
        return categories_list

    def add_category(self, _new_category):
        self.categories.push(_new_category)

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
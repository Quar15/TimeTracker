import json
import sys, os
import pygetwindow as gw

print(gw.getActiveWindow().title)

class TimeTracker:

    def __init__(self):
        self.activities = []

    def initialize_me(self):
        if(os.path.isfile("./TimeTrackerData.json")):
            with open("./TimeTrackerData.json", "r"):
                data = json.load(f)
                self.activities.append(self.get_activities_from_json(data))

    def get_activities_from_json(self, data):
        activity_list = []
        for activity in data['activities']:
            activity_list.append(
                Activity(activity["name"], self.get_categories_from_json(activity), activity['total_time_spend'])
            )

        return activity_list



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
            "categories": self.serialize_categories_to_json()
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
    def __init__(self, _window_name):
        self.window_name = _window_name
        self.time_spend = 0


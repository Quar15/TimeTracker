import json
import os
from datetime import datetime


class TimeTracker:

    def __init__(self):
        self.activities = []
        self.categories = []

    def initialize_me(self):
        if os.path.isfile("./data/TimeTrackerData.json") and os.path.isfile("./data/TimeTrackerCategories.json"):
            with open("./data/TimeTrackerData.json", "r") as f:
                data = json.load(f)
                self.activities = self.get_activities_from_json(data)

            with open("./data/TimeTrackerCategories.json", "r") as f:
                data = json.load(f)
                self.categories = self.get_categories_from_json(data)
        else:
            print("Welcome to Time Tracker!")

    def get_activities_from_json(self, data):
        activity_list = []
        for activity in data['activities']:
            activity_list.append(
                Activity(activity['name'], activity['categories_id'], activity['total_time_spend'])
            )
        return activity_list

    def get_categories_from_json(self, data):
        category_list = []
        for category in data['categories']:
            category_list.append(ActivityCategory(category['id'], category['name'], category['wage'], category['total_time_spend'], category['keywords']))
        return category_list

    def add_activity(self, new_activity):
        self.activities.append(new_activity)

    def add_category(self, new_category):
        self.categories.append(new_category)

    def update_all_activities_categories(self):
        for activity in self.activities:
            for category in self.categories:
                for keyword in category.keywords:
                    if keyword in activity.name:
                        activity.add_category(category.id)

    def update_all_categories_time_spend(self):
        for category in self.categories:
            new_total_time_spend = 0
            for activity in self.activities:
                if category.id in activity.categories_id:
                    new_total_time_spend += activity.total_time_spend

            category.total_time_spend = new_total_time_spend

    def search_for_activity(self, searched_activity_window_name, time_spend):
        for activity in self.activities:
            if activity.name == searched_activity_window_name:
                activity.total_time_spend += time_spend
                return activity
        return None

    def search_category_by_id(self, searched_category_id):
        for category in self.categories:
            if category.id == searched_category_id:
                return category
        return None

    def search_category_by_name(self, searched_category_name):
        for category in self.categories:
            if category.name == searched_category_name:
                return category
        return None

    def update_category(self, id, name=None, wage=None, keywords=[], time_spend=None):
        
        changed_category = self.search_category_by_id(id)

        if changed_category != None:
            if name != None:
                changed_category.name = name
            if wage != None:
                changed_category.wage = wage
            if keywords != []:
                changed_category.keywords = keywords
            if time_spend != None:
                changed_category.total_time_spend = time_spend

            self.categories[changed_category.id] = changed_category 
            print("Category ID =", changed_category.id, "updated!")

    def update_category_force(self, category):
        self.categories[category.id] = category
        print("Force ActivityCategory ID =", category.id, "update completed!")

    def serialize_list_to_json(self, list_to_serialize):
        object_list = []
        for obj in list_to_serialize:
            object_list.append(obj.serialize())
        return object_list

    def save_to_json(self, path, serialized_data):
        with open(path, "w") as f:
            json.dump(serialized_data, f, indent=4, sort_keys=True)

    def save_me(self):
        self.save_to_json("./data/TimeTrackerData.json", {"activities": self.serialize_list_to_json(self.activities)})
        self.save_to_json("./data/TimeTrackerCategories.json", {"categories": self.serialize_list_to_json(self.categories)})


class ActivityCategory:

    def __init__(self, _id, _name, _wage, _total_time_spend=0, _keywords = []):
        self.id = _id
        self.name = _name
        self.wage = _wage
        self.total_time_spend = _total_time_spend
        self.keywords = _keywords

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "wage": self.wage,
            "total_time_spend": self.total_time_spend,
            "keywords": self.keywords
        }

    def add_keywords(self, new_keywords):
        print(self.keywords)
        for new_keyword in new_keywords:
            if new_keyword not in self.keywords:
                self.keywords.append(new_keyword)
                print("New keyword added to", self.name)

class Activity:
    
    def __init__(self, _name, _categories_id, _total_time_spend=0):
        self.name = _name
        self.categories_id = _categories_id
        self.total_time_spend = _total_time_spend

    def serialize(self):
        return {
            "name": self.name,
            "categories_id": self.categories_id,
            "total_time_spend" : self.total_time_spend
        }

    def add_category(self, new_category_id):
        if new_category_id not in self.categories_id:
            self.categories_id.append(new_category_id)
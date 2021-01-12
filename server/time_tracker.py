import json
import os
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt


def serialize_list_to_json(list_to_serialize):
    object_list = []
    for obj in list_to_serialize:
        object_list.append(obj.serialize())
    return object_list

def save_to_json(path, serialized_data):
    with open(path, "w") as f:
        json.dump(serialized_data, f, indent=4, sort_keys=True)

def get_readable_time(seconds):
    readable_time = str(timedelta(seconds=seconds))
    return(readable_time)

class TimeTracker:

    def __init__(self, days_to_subtract=0, date=None):
        self.activities = []
        if date == None:
            self.date = (datetime.today() - timedelta(days=days_to_subtract)).strftime("%d%m%Y")
        else:
            self.date = date
        self.file_name = "./data/TimeTrackerData" + self.date + ".json"

    def __str__(self):
        str_representation = "TimeTracker object " + self.date
        return str_representation

    def __repr__(self):
        str_representation = "TimeTracker object " + self.date
        return str_representation

    def initialize_me(self):
        if os.path.isfile(self.file_name) and os.path.isfile("./data/TimeTrackerCategories.json"):
            with open(self.file_name, "r") as f:
                data = json.load(f)
                self.activities = self.get_activities_from_json(data)
        else:
            raise IOError("WARNING: File " + self.file_name + " not found!")

    def get_activities_from_json(self, data):
        activity_list = []
        for activity in data['activities']:
            activity_list.append(
                Activity(activity['name'], activity['categories_id'], activity['total_time_spend'])
            )
        return activity_list

    def get_readable_date(self):
        return (self.date[0:2]+"."+self.date[2:4]+"."+self.date[4:])

    def get_categories_and_time(self, serialize_time=False):
        temp_categories = TimeTrackerCategories()
        temp_categories.initialize_me()
        temp_categories.update_all_categories_time_spend(self.activities)
        categories = temp_categories.categories

        category_times = []
        category_names = []
        for category in categories:
            category_names.append(category.name)
            total_time_spend = category.total_time_spend
            if(serialize_time):
                total_time_spend = get_readable_time(total_time_spend)
            category_times.append(total_time_spend)

        return category_times, category_names

    def add_activity(self, new_activity):
        self.activities.append(new_activity)

    def create_graph(self, create_legend_png=False):
        graph_file_name = "./static/png/TimeTrackerData" + self.date + ".png"
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        category_time, category_names = self.get_categories_and_time()

        def get_labels(allvals):
            labels = []
            for val in allvals:
                percent_val = float(val/np.sum(allvals)*100.)
                labels.append("{:.1f}%".format(percent_val))
            return labels


        wedges, texts, autotexts = ax.pie(category_time, autopct="", textprops=dict(color="w"), labels=get_labels(category_time))


        if create_legend_png:
            my_legend = ax.legend(wedges, category_names,
                    title="Categories",
                    loc="center left",
                    bbox_to_anchor=(1, 0, 0.5, 1))
            legend_fig = my_legend.figure
            legend_fig.canvas.draw()
            bbox = my_legend.get_window_extent().transformed(legend_fig.dpi_scale_trans.inverted())
            legend_fig.savefig("./static/png/categories-legend.png", dpi="figure", bbox_inches=bbox, transparent=True)
            my_legend.remove()

        plt.setp(autotexts, size=8, weight="bold")
        plt.savefig(graph_file_name, bbox_inches='tight', transparent=True)

    def update_activity_categories(self, activity):
        for category in self.categories:
            for keyword in category.keywords:
                if keyword in activity.name and category.id not in activity.categories_id:
                    activity.add_category(category.id)

    def update_all_activities_categories(self, categories):
        for activity in self.activities:
            for category in categories:
                for keyword in category.keywords:
                    if keyword in activity.name:
                        activity.add_category(category.id)

    def search_for_activity(self, searched_activity_window_name, time_spend):
        for activity in self.activities:
            if activity.name == searched_activity_window_name:
                activity.total_time_spend += time_spend
                return activity
        return None

    def save_me(self):
        save_to_json(self.file_name, {"activities": serialize_list_to_json(self.activities)})


class TimeTrackerCategories:

    def __init__(self):
        self.categories = []

    def initialize_me(self):
        # read data from json
        with open("./data/TimeTrackerCategories.json", "r") as f:
            data = json.load(f)

        # initialize categories (serialize data from json)
        self.categories = self.get_categories_from_json(data)

    def get_categories_from_json(self, data):
        category_list = []
        subcategories = []

        # read data from json and create categories
        for category in data['categories']:
            new_category = (ActivityCategory(category['id'], category['name'], category['wage'], category['total_time_spend'], category['overcategory'], category['keywords']))
            if new_category.overcategory == -1:
                category_list.append(new_category)
            elif new_category.overcategory >= 0:
                subcategories.append(new_category)

        # handle subcategories 
        for subcategory in subcategories:
            category_list[subcategory.overcategory].add_subcategory(subcategory)

        return category_list

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

    def create_category(self, name, wage, keywords):
        new_category = ActivityCategory(len(self.categories), name, wage, 0, keywords)
        if self.search_category_by_name(new_category.name) == None:
            self.add_category(new_category)

    def add_keywords_to_category(self, category_id, new_keywords):
        changed_category = self.search_category_by_id(category_id)
        if changed_category != None:
            changed_category.add_keywords(new_keywords)
            self.update_category_force(changed_category)
        else:
            print("WARNING: Category NOT found!")

    def add_category(self, new_category):
        self.categories.append(new_category)

    def update_all_categories_time_spend(self, activities):
        for category in self.categories:
            new_total_time_spend = 0
            for activity in activities:
                if category.id in activity.categories_id:
                    new_total_time_spend += activity.total_time_spend

            category.total_time_spend = new_total_time_spend

    def update_all_categories_time_spend_force(self, new_times_spend):
        try:
            for category, new_time_spend in zip(self.categories, new_times_spend):
                category.total_time_spend = new_time_spend
        except:
            print("ERROR: new_times_spend length is not equal length of TimeTrackerCategories.categories")

    def update_category_force(self, category):
        self.categories[category.id] = category
        print("Force ActivityCategory ID =", category.id, "update completed!")

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

    def save_me(self):
        save_to_json("./data/TimeTrackerCategories.json", self.serialize())

    def serialize(self):
        return ({"categories": serialize_list_to_json(self.categories)})

class ActivityCategory:

    def __init__(self, _id, _name, _wage, _total_time_spend=0, _overcategory = -1, _keywords = []):
        self.id = _id
        self.name = _name
        self.wage = _wage
        self.total_time_spend = _total_time_spend
        self.keywords = _keywords
        self.overcategory = _overcategory
        self.subcategories = []

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "wage": self.wage,
            "total_time_spend": self.total_time_spend,
            "overcategory": self.overcategory,
            "keywords": self.keywords
        }

    def add_keywords(self, new_keywords):
        print(self.keywords)
        for new_keyword in new_keywords:
            if new_keyword not in self.keywords:
                self.keywords.append(new_keyword)
                print("New keyword added to", self.name)

    def add_subcategory(self, new_subcategory):
        for subcategory in self.subcategories:
            if subcategory == new_subcategory:
                return False
        self.subcategories.append(new_subcategory)
        return True


class Activity:
    
    def __init__(self, _name, _categories_id, _total_time_spend=0):
        self.name = _name
        self.categories_id = _categories_id
        self.total_time_spend = _total_time_spend

    def serialize(self):
        return {
            "name": self.name,
            "categories_id": self.categories_id,
            "total_time_spend" : int(self.total_time_spend)
        }

    def get_readable_time(self):
        readable_time = str(timedelta(seconds=self.total_time_spend))
        return(readable_time)

    def add_category(self, new_category_id):
        if new_category_id not in self.categories_id:
            self.categories_id.append(new_category_id)
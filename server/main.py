from time_tracker import *
import sys

def update_activity_categories(activity):
    for category in time_tracker.categories:
        for keyword in category.keywords:
            if keyword in activity.name and category.id not in activity.categories_id:
                activity.add_category(category.id)


def create_category(name, wage, keywords):
    new_category = ActivityCategory(len(time_tracker.categories), name, wage, 0, keywords)
    if time_tracker.search_category_by_name(new_category.name) == None:
        time_tracker.add_category(new_category)
        time_tracker.update_all_activities_categories()


def add_keywords_to_category(category_id, new_keywords):
    changed_category = time_tracker.search_category_by_id(category_id)
    if changed_category != None:
        changed_category.add_keywords(new_keywords)
        time_tracker.update_category_force(changed_category)
    else:
        print("WARNING: Category NOT found!")


time_tracker = TimeTracker()

try:
    time_tracker.initialize_me()
except json.decoder.JSONDecodeError:
    print("\nFailed to load data from ./TimeTrackerData.json")


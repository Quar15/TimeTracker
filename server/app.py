from time_tracker import *
import sys

from flask import Flask, render_template, request
app = Flask(__name__)

DAYS_TO_LOAD = 7

def initialize_time_trackers():
    time_trackers = []
    for i in range(DAYS_TO_LOAD):
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


def update_categories_in_time_trackers():
    for time_tracker in time_trackers:
        time_tracker.update_all_activities_categories(time_tracker_categories_obj.categories)
        time_tracker_categories_obj.update_all_categories_time_spend(time_tracker.activities)


def save_data():
    for time_tracker in time_trackers:
        time_tracker.save_me()


def update_data():
    update_categories_in_time_trackers()
    save_data()
    print("INFO: Data updated")


def get_time_tracker_by_date(searched_date):
    for time_tracker in time_trackers:
        if time_tracker.date == searched_date:
            return time_tracker
    return None


def create_graphs_for_time_trackers():
    for time_tracker in time_trackers:
        time_tracker.create_graph()


def create_legend():
    time_trackers[0].create_graph(create_legend_png=True)


time_tracker_categories_obj = initialize_categories()
time_trackers = initialize_time_trackers()
update_data()
if len(time_trackers):
    create_graphs_for_time_trackers()
    create_legend()
    pass

@app.route('/')
def index():
    graph_files = []
    graph_dates = []
    for time_tracker in time_trackers:
        graph_dates.append(time_tracker.get_readable_date())
        graph_files.append("/png/TimeTrackerData" + time_tracker.date + ".png")
    return render_template("index.html", graph_data=zip(graph_files, graph_dates))


@app.route('/create-category')
def create_category_html():
    return render_template("create-category.html")


@app.route('/browse-all')
def browse_all():
    return render_template("browse-all.html", time_trackers=time_trackers)


@app.route("/send-data", methods=['POST'])
def add_new_data():
    try:
        new_time_tracker_data = request.get_json()
        new_time_tracker = TimeTracker(date=new_time_tracker_data['date'])
        new_time_tracker.activities = new_time_tracker.get_activities_from_json(new_time_tracker_data)
        time_trackers.append(new_time_tracker)
        update_data()
        return ""
    except:
        print("ERROR: File error")
        return "Error with files"


@app.route("/get-categories")
def get_categories():
    return {"categories": time_tracker_categories_obj.serialize()}


@app.route("/get-category-by-id/<searched_category_id>")
def get_category_by_id(searched_category_id):
    output = []
    searched_category = time_tracker_categories_obj.search_category_by_id(int(searched_category_id))
    if searched_category != None:
        output = searched_category.serialize()
    return {"category": output}


@app.route('/get-time-trackers')
def get_data():
    output = []
    for time_tracker in time_trackers:
        output.append({time_tracker.date : {"activities": serialize_list_to_json(time_tracker.activities)}})

    return {"time_trackers": output}


@app.route('/get-time-trackers/<date>')
def get_data_with_date(date):
    output = ""
    searched_time_tracker = get_time_tracker_by_date(date)
    if searched_time_tracker != None:
        output = {"activities": serialize_list_to_json(searched_time_tracker.activities)}
    
    return {"time_tracker": output}
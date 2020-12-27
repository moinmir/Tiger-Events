from flask import render_template, request, Blueprint
from tigerevents.models import Event, Saved
from flask_login import login_user, current_user, login_required


main = Blueprint('main', __name__)

@main.route("/")  # home page
@main.route("/home")
@login_required
def home():
    myevents = current_user.going_to()
    org_events = current_user.org_events()
    all_events = Event.query.all()
    events = [event for event in all_events if event not in myevents]
    org_events = [event for event in org_events if event not in myevents]
    events = [event for event in events if event not in org_events]
    return render_template("home.html", events=events, org_events=org_events, title="Home")

@main.route("/search")
def search():
    print(Event.query.search('Study').limit(5).all)
    return render_template("search.html")

@main.route("/about") 
def about():
    return render_template("about.html", title="About")

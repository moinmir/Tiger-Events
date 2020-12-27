from flask import render_template, request, Blueprint
from tigerevents.models import Event, Saved
from flask_login import login_user, current_user, login_required
from tigerevents import db
from tigerevents.main.forms import SearchForm

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

    form = SearchForm()

    return render_template("home.html", events=events, org_events=org_events, title="Home", form=form)

@main.route("/search")
def search():
    searchq = request.args.get('searchq')
    events = Event.query.filter(Event.title.ilike('%' + searchq + '%')).all()
    
    form = SearchForm()
    
    return render_template("search.html", events=events, form=form)

@main.route("/about") 
def about():
    return render_template("about.html", title="About")

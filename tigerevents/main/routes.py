from flask import render_template, request, Blueprint, json
from tigerevents.models import Event, Saved
from flask_login import current_user
from tigerevents.utils import login_required
from tigerevents.main.forms import SearchForm

main = Blueprint('main', __name__)

@main.route("/")  # home page
@main.route("/home")
@login_required(role='ANY')
def home():
    # home page for host is different
    if current_user.urole == "Host":
        return render_template("org_events.html", title="My Events", events=current_user.hosting, link=current_user.get_link())

    myevents = current_user.going_to()
    org_events = current_user.org_events()
    all_events = Event.query.all()
    events = [event for event in all_events if event not in myevents]
    org_events = [event for event in org_events if event not in myevents]
    events = [event for event in events if event not in org_events]

    form = SearchForm()

    return render_template("home.html", events=events, org_events=org_events, title="Home", form=form)

@main.route("/home/json")
@login_required
def home2():
    myevents = current_user.going_to()
    org_events = current_user.org_events()
    all_events = Event.query.all()
    events = [event for event in all_events if event not in myevents]
    org_events = [event for event in org_events if event not in myevents]
    events = [event for event in events if event not in org_events]

    return json.jsonify(
        {"events" : [
            {
                "id": i,
                "title" : event.title,
                "hostname" : event.host.name,
                "location" : event.location,
                "startdate" : event.start_date.strftime("%a %b %-d, %I:%M%p"),
                "enddate" : event.end_date.strftime("%I:%M%p"),
                "description": event.description
            } for (i, event) in zip(range(len(events)), events)]
        }
        
    )

    #n=len(events),
    #titles= [event.title for event in events],
    #hostnames= [event.host.name for event in events],
    #locations= [event.location for event in events],
    #startdates = [event.start_date.strftime("%a %b %-d, %I:%M%p") for event in events],
    #enddates = [event.end_date.strftime("%I:%M%p") for event in events]

@main.route("/search")
def search():
    searchq = request.args.get('searchq')
    events = Event.query.filter(Event.title.ilike('%' + searchq + '%')).all()
    events.extend(Event.query.filter(Event.description.ilike('%' + searchq + '%')).all())
    events.extend(Event.query.filter(Event.location.ilike('%' + searchq + '%')).all())
    
    form = SearchForm()
    
    return render_template("search.html", events=events, form=form)

@main.route("/about") 
def about():
    return render_template("about.html", title="About")

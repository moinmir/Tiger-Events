from flask import render_template, request, Blueprint
from tigerevents.models import Event, Saved
from flask_login import login_user, current_user, login_required


main = Blueprint('main', __name__)

@main.route("/")  # home page
@main.route("/home")
@login_required
def home():
    page = request.args.get("page", 1, type=int)
    events = Event.query.order_by(Event.date_posted.desc()).paginate(per_page=5, page=page)
    myevents = [assoc.event for assoc in current_user.events]
    # [assoc.event for assoc in Saved.query.filter_by(user_id = current_user.id).all()]
    return render_template("home.html", events=events, myevents=myevents,  title="Home")

@main.route("/search")
def search():
    return render_template("search.html")

@main.route("/about") 
def about():
    return render_template("about.html", title="About")

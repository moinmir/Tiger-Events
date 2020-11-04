from flask import render_template, request, Blueprint
from tigerevents.models import Event


main = Blueprint('main', __name__)

@main.route("/")  # home page
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    events = Event.query.order_by(Event.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template("home.html", events=events, title="Home")


@main.route("/about") 
def about():
    return render_template("about.html", title="About")

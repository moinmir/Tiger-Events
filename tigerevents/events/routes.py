from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user
from tigerevents import db
from tigerevents.models import Event

events = Blueprint("events", __name__)

@events.route("/event/<int:event_id>")
def event(campaign_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event.html", title=event.title, event=event)

from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_user, current_user, login_required
from tigerevents import db
from tigerevents.models import Event, User, Saved


events = Blueprint("events", __name__)

@events.route("/event/<int:event_id>")
def event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event.html", title=event.title, event=event)

@events.route("/event/save/<int:event_id>")
@login_required
def save(event_id):
    event = Event.query.get_or_404(event_id)

    if event is None:
        flash(
            message="Event not found.", 
            category="danger"
        )
        return redirect(url_for("main.home"))

    save1 = Saved(going=False)
    save1.event = event
    save1.user = current_user
    db.session.add(save1)
    db.session.commit()

    flash(
        message=f"Successfully saved {event.title}",
        category="success",
    )

    return redirect(url_for("main.home"))


@events.route("/event/rsvp/<int:event_id>")
@login_required
def rsvp(event_id):
    event = Event.query.get_or_404(event_id)

    if event is None:
        flash(
            message="Event not found.", 
            category="danger"
        )
        return redirect(url_for("main.home"))

    save1 = Saved(going=True)
    save1.event = event
    save1.user = current_user
    db.session.add(save1)
    db.session.commit()

    flash(
        message=f"Successfully saved {event.title}",
        category="success",
    )

    return redirect(url_for("main.home"))

@events.route("/event/remove/<int:event_id>")
@login_required
def remove(event_id):
    event = Event.query.get_or_404(event_id)

    if event is None:
        flash(
            message="Event not found.", 
            category="danger"
        )
        return redirect(url_for("main.home"))

    
    assoc = Saved.query.filter_by(user_id = current_user.id).filter_by(event_id = event_id)[0]
    db.session.delete(assoc)
    db.session.commit()

    flash(
        message=f"Successfully removed {event.title}",
        category="success",
    )

    return redirect(url_for("users.myevents"))
    

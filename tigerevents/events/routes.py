from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_user, current_user
from tigerevents import db
from tigerevents.models import Event, User, Saved
from tigerevents.events.utils import login_required
from tigerevents.events.forms import EventForm


events = Blueprint("events", __name__)

@events.route("/event/<int:event_id>")
def event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event.html", title=event.title, event=event)

@events.route("/event/save/<int:event_id>")
@login_required(role='ANY')
def save(event_id):
    event = Event.query.get_or_404(event_id)

    if event is None:
        flash(
            message="Event not found.", 
            category="danger"
        )
        return redirect(url_for("main.home"))
    elif current_user.is_saved(event):
        flash(
            message="Already saved.", 
            category="danger"
        )
        return redirect(url_for("main.home"))
    
    elif current_user.clash(event):
        flash(
            message="Clashes with an event in your calendar.", 
            category="danger"
        )

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
@login_required(role='ANY')
def rsvp(event_id):
    event = Event.query.get_or_404(event_id)

    if event is None:
        flash(
            message="Event not found.", 
            category="danger"
        )
        return redirect(url_for("main.home"))
    
    elif current_user.is_going(event):
        flash(
            message="Event already added.", 
            category="danger"
        )
        return redirect(url_for("users.myevents"))

    elif current_user.clash(event):
        flash(
            message="Clashes with an event in your calendar.", 
            category="danger"
        )
        return redirect(url_for("users.myevents"))

    elif current_user.is_saved(event):
        Saved.query.filter_by(event_id = event_id).filter_by(user_id = current_user.id)[0].going = True
        db.session.commit()
        flash(
            message="Event added to calendar.", 
            category="success"
        )
        return redirect(url_for("users.myevents"))

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
@login_required(role='ANY')
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


@events.route("/event/delete/<int:event_id>", methods=["POST"])
@login_required(role="Host")
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event is None:
        flash(
            message="Event not found.", 
            category="danger"
        )
        return redirect(url_for("main.home"))

    db.session.delete(event)
    db.session.commit()

    flash(
        message=f"Successfully deleted {event.title}",
        category="success",
    )

    return redirect(url_for("users.myevents"))


@events.route("/event/new", methods=["GET", "POST"])
@login_required(role="Host")
def new_event(event_id):
    form = EventForm()

    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            host=current_user.host_of(),
        )
        db.session.add(event)
        db.session.commit()

        flash("Your event has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template(
        "create_event.html", title="New Event", form=form, legend="New Event"
    )

    flash(
        message=f"Successfully deleted {event.title}",
        category="success",
    )

    return redirect(url_for("users.myevents"))



    

from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user
from tigerevents import db
from tigerevents.models import Event, Saved
from tigerevents.utils import login_required
from tigerevents.events.forms import EventForm


events = Blueprint("events", __name__)

@events.route("/event/<int:event_id>")
def event(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event.html", title=event.title, event=event)

@events.route("/event/save/<int:event_id>")
@login_required(role='User')
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
@login_required(role='User')
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
        return redirect(url_for("main.home"))

    elif current_user.clash(event):
        flash(
            message="Clashes with an event in your calendar.", 
            category="danger"
        )
        return redirect(url_for("main.home"))

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
@login_required(role='User')
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
@login_required(role="ANY")
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event is None:
        flash(
            message="Event not found.", 
            category="danger"
        )
        return redirect(url_for("main.home"))

    if event.creator == current_user:
        db.session.delete(event)
        db.session.commit()

        flash(
            message=f"Successfully deleted {event.title}",
            category="success",
        )
    else:
        flash(
            message="No authorization.", 
            category="danger"
        )

    return redirect(url_for("users.myevents"))


@events.route("/event/new", methods=["GET", "POST"])
@login_required(role="ANY")
def new_event():
    form = EventForm()

    if form.validate_on_submit():
        new_event = Event(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            host=current_user.org,
            creator=current_user
        )
        db.session.add(new_event)
        db.session.commit()

        flash("Your event has been created!", "success")
        return redirect(url_for("users.myevents"))
    return render_template('create_event.html', title='New Event',
                           form=form, legend='New Event')

@events.route("/event/edit/<int:event_id>", methods=["GET", "POST"])
@login_required(role="ANY")
def edit_event(event_id):
    form = EventForm()
    event = Event.query.filter_by(id=event_id)

    if form.validate_on_submit():
    
        event.title = form.title.data
        event.description = form.description.data
        event.location = form.location.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data
        
        db.session.commit()
        flash("Your event has been updated!", "success")
        if current_user.urole == 'User':
            return redirect(url_for("users.myevents"))
        else:
            return redirect(url_for("main.home"))

    # elif request.method == 'GET':

    #     form.title.data = event.title
    #     form.description.data = event.description
    #     form.location.data = event.location
    #     form.start_date.data = event.start_date
    #     form.end_date.data = event.end_date
        
    return render_template('create_event.html', title='Edit Event',
                           form=form, legend='Edit Event')
from flask import (
    render_template, 
    url_for, 
    flash, 
    redirect, 
    request, 
    Blueprint,
    send_file, send_from_directory, safe_join, abort,
    current_app,
)
from flask_login import login_user, current_user, logout_user, login_required
from tigerevents import db, bcrypt
from tigerevents.models import User, Event, Saved
from tigerevents.users.forms import (
    RegistrationForm,
    LoginForm,
    RequestResetForm,
    ResetPasswordForm,
)
from tigerevents.users.cal import create_ical, save_ical
import uuid

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()

    if form.validate_on_submit():
        # created user and adding to database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()

        flash(
            message="Your account has been created! You can now log in",
            category="success",
        )
        return redirect(url_for("users.login"))

    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful. Please check email and password.", "danger")

    return render_template("login.html", title="Login", form=form)


@users.route("/myevents", methods=["GET", "POST"])
@login_required
def myevents():
    # events followed by user
    events = current_user.events
    
    return render_template("myevents.html", title="My Events", events=events)

    
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/myevents/ical/<uuid:ical_uuid>", methods=["GET", "POST"])
@login_required
def download_ical(ical_uuid):
    events = current_user.going_to()
    cal = create_ical(events)
    ical_fn = save_ical(current_user, cal)
    try:
        return send_from_directory(current_app.config["USER_CAL"], filename=ical_fn, as_attachment=True)
    except FileNotFoundError:
        abort(404)

# @users.route("/myevents/ical", methods=["GET", "POST"])
# @login_required
# def get_ical_link():
#     link = current_user.ical_uuid.hex + '.ics'
    
    

   
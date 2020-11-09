from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from tigerevents import db, bcrypt
from tigerevents.models import User, Event
from tigerevents.users.forms import (
    RegistrationForm,
    LoginForm,
    RequestResetForm,
    ResetPasswordForm,
)

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
            next_page = request.args.get("next")
            return (
                redirect(url_for(next_page[1:]))
                if next_page
                else redirect(url_for("main.home"))
            )
        else:
            flash("Login Unsuccessful. Please check email and password.", "danger")

    return render_template("login.html", title="Login", form=form)


@users.route("/myevents", methods=["GET", "POST"])
@login_required
def myevents():
    events = Event.query
    return render_template(
        "myevents.html", title="My Events", events=events
    )


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))




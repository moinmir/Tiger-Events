from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_user, current_user, login_required
from tigerevents import db
from tigerevents.models import Organization, User

organizations = Blueprint("organizations", __name__)

@organizations.route("/organizations")
@login_required
def org_page():
    # organizations followed by the user
    myorgs = [assoc.organization for assoc in current_user.following]
    # Organization.query.join(a_follow).join(User).filter(a_follow.c.user_id == current_user.id).all()

    # organizations not followed by the user
    unorgs = Organization.query.all()
    unorgs = [org for org in unorgs if org not in myorgs]
    
    return render_template("organizations.html", title="Organizations", myorgs=myorgs, unorgs=unorgs, user=current_user)

@organizations.route("/organizations/follow/<int:org_id>")
@login_required
def follow(org_id):
    org = Organization.query.get_or_404(org_id)
    if org is None:
        flash(
            message="Organization not found.", 
            category="danger"
        )
        return redirect(url_for("organizations.org_page"))
    
    u = current_user.follow(org)
    if u is None:
        flash(
            message=f"Cannot follow {org.name}",
            category="danger"
        )
        return redirect(url_for("organizations.org_page"))

    db.session.add(u)
    db.session.commit()
    flash(
        message=f"You are now following {org.name}",
        category="success",
    )
    return redirect(url_for("organizations.org_page"))


@organizations.route("/organizations/unfollow/<int:org_id>")
@login_required
def unfollow(org_id):
    org = Organization.query.get_or_404(org_id)
    if org is None:
        flash(
            message="Organization not found.", 
            category="danger"
        )
        return redirect(url_for("organizations.org_page"))
    
    u = current_user.unfollow(org)
    if u is None:
        flash(
            message=f"Cannot unfollow {org.name}",
            category="danger"
        )
        return redirect(url_for("organizations.org_page"))

    db.session.add(u)
    db.session.commit()
    flash(
        message=f"You have stopped following {org.name}",
        category="success",
    )
    return redirect(url_for("organizations.org_page"))

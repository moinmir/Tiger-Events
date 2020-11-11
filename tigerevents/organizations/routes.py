@organizations.route("/organizations", methods=["GET", "POST"])
@login_required
def organizations():
    # organizations followed by the user
    myorgs = [org for org in current_user.following]

    # organizations not followed by the user
    unorgs = Organization.query.all()
    unorgs = [org for org in unorg if org not in myorgs]
    
    return render_template("organizations.html", title="Organizations", myorgs=myorgs, unorgs=unorgs)
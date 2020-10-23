from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tigerevents import db, login_manager
from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# class models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # many to many relationships
    maybe_e = db.relationship("Event", secondary="saved")
    going_e = db.relationship("Event", secondary="going")
    following = db.relationship("Organization", secondary="follow")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.email}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default_campaign.jpg")
    
    # relationships - many to many
    maybe_u = db.relationship("User", secondary="saved") 
    going_u = db.relationship("User", secondary="going")
    tags = db.relationship("Tag", secondary="event_tags")

    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=False)


    def __repr__(self):
        return f"Event('{self.title}', '{self.date_posted}', '{self.host}')"


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default_organization.jpg")
    description = db.Column(db.Text, nullable=False)

    # relationships
    tags = db.relationship("Tag", secondary="org_tags")
    events = db.relationship("Event", backref="host", lazy=True)

    def __repr__(self):
        return f"Campaign('{self.name}', '{self.events}')"

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    # relationships
    events = db.relationship("Event", secondary="event_tag")
    organizations = db.relationship("Organization", secondary="org_tag")



# association tables

# 1. Events saved by user
class Saved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    user = db.relationship(User, backref=db.backref("saved", cascade="all, delete-orphan"))
    event = db.relationship(Event, backref=db.backref("saved", cascade="all, delete-orphan"))
    
# 2. Events user is going to 
class Going(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    user = db.relationship(User, backref=db.backref("going", cascade="all, delete-orphan"))
    event = db.relationship(Event, backref=db.backref("going", cascade="all, delete-orphan"))


# 3. Organizations followed by user
class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    org_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship(User, backref=db.backref("follow", cascade="all, delete-orphan"))
    org = db.relationship(Event, backref=db.backref("follow", cascade="all, delete-orphan"))

# 4. Event tags
class Event_tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    event = db.relationship(User, backref=db.backref("event_tags", cascade="all, delete-orphan"))
    tag = db.relationship(Event, backref=db.backref("event_tags", cascade="all, delete-orphan"))

# 5. Organization tags
class Org_tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    event = db.relationship(User, backref=db.backref("org_tags", cascade="all, delete-orphan"))
    tag = db.relationship(Event, backref=db.backref("org_tags", cascade="all, delete-orphan"))
    


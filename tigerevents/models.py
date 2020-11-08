from datetime import datetime
from tigerevents import db, login_manager
from flask_login import UserMixin

# get user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#####################################################################
# Association Models/Tables                                         #
#####################################################################
# 1. Events saved by user
class Saved(db.Model):
    __tablename__ = 'a_saved'
    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('nice_user.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('nice_event.id'), primary_key=True)

    # extra data
    going = db.Column(db.Boolean, unique=False, default=False)

    event = db.relationship("Event", back_populates="participants" )
    user = db.relationship("User", back_populates="events")

a_follow = db.Table("follow",
                    db.Column("user_id", db.Integer, db.ForeignKey('nice_user.id')),
                    db.Column("org_id", db.Integer, db.ForeignKey('nice_organization.id'))
                   )

#####################################################################

#####################################################################
# Class Models                                                      #
#####################################################################
class User(db.Model, UserMixin):
    __tablename__ = 'nice_user'
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # relationships - all many to many
    # association object
    events = db.relationship("Saved", 
                             back_populates="user", 
                             cascade="all, delete-orphan")

    # association table
    following = db.relationship("Organization",
                             secondary=a_follow,
                             back_populates="followers",
                                ) 
                           
    # functions/methods
    def __repr__(self):
        return f"User('{self.email}')"
#####################################################################

####################################################################
class Event(db.Model):
    __tablename__='nice_event'
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default_campaign.jpg")
    
    # relationships
    # association object
    participants = db.relationship("Saved", 
                                   back_populates="event", 
                                   cascade="all, delete-orphan")
    
    org_id = db.Column(db.Integer, db.ForeignKey("nice_organization.id"), nullable=False)

    # functions/methods
    def __repr__(self):
        return f"Event('{self.title}', '{self.date_posted}')"
#####################################################################

####################################################################

####################################################################
class Organization(db.Model):
    __tablename__='nice_organization'

    # attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default_campaign.jpg")

    # relationships
    # followers = db.relationship("User", secondary='follow') 
    events = db.relationship("Event", backref="host", lazy=True)

    followers = db.relationship("User",
                                secondary=a_follow,
                                back_populates="following",
                                )
    
    tags = db.relationship("Tag",
                           secondary=org_tags,
                           back_populates="organizations")

    # functions/methods
    def __repr__(self):
        return f"Event('{self.name}', '{self.date_created}')"
####################################################################

# class Tag(db.Model):
#     __tablename__='nice_tag'

#     # attributes
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)

#     # relationship
#     organizations = db.relationship("Organization",
#                                     secondary=org_tags,
#                                     back_populates="tags")

####################################################################

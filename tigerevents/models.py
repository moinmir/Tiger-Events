from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tigerevents import db, login_manager
from flask import current_app
from flask_login import UserMixin
from sqlalchemy import create_engine

# get user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

####################################################################
#    Association Tables/Objects                                    #
####################################################################

# 1. Events saved by user
class Saved(db.Model):

    # foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), primary_key=True)

    # extra data
    going = db.Column(db.Boolean, unique=False, default=True)

    user = db.relationship("User", back_populates="events")
    event = db.relationship("Event", back_populates="participants" )

# 2. Organizations followed by user
follow = db.Table('follow', 
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                  db.Column('org_id', db.Integer, db.ForeignKey('organization.id'))
                 ) 

# 3. Event tags
event_tags = db.Table('event_tags',
                      db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
                      db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                     ) 

# 4. Organization tags
org_tags = db.Table('org_tags',
                    db.Column('org_id', db.Integer, db.ForeignKey('organization.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                   ) 

# 5. User tags
user_tags = db.Table('user_tags',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                    ) 
    
####################################################################

####################################################################
#    Class Models                                                  #
####################################################################

####################################################################
class Event(db.Model):
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

    # association table
    tags = db.relationship("Tag", 
                           secondary="event_tags", 
                           back_populates="events")

    # foreign key for relation with organization
    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=False)

    # functions/methods
    def __repr__(self):
        return f"Event('{self.title}', '{self.date_posted}', '{self.host}')"

####################################################################

####################################################################
class User(db.Model, UserMixin):
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # relationships - all many to many
    # association object
    events = db.relationship(Saved, 
                             back_populates="user", 
                             cascade="all, delete-orphan") 

    # association table
    following = db.relationship("Organization", 
                                secondary="follow", 
                                back_populates="followers", 
                                cascade="all, delete-orphan") 

    # association table
    tags = db.relationship("Tag", 
                           secondary="user_tags", 
                           back_populates="users", 
                           cascade="all, delete-orphan")
                           
    # functions/methods
    def __repr__(self):
        return f"User('{self.email}')"

####################################################################

####################################################################
class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default_organization.jpg")
    description = db.Column(db.Text, nullable=False)

    # relationships
    # association table
    tags = db.relationship("Tag", 
                           secondary="org_tags", 
                           back_populates="organizations", 
                           cascade="all, delete-orphan")

    # association table
    followers = db.relationship("User", 
                                secondary='follow', 
                                back_populates="organizations", 
                                cascade="all, delete-orphan")

    # one (organization) to many (events)
    events = db.relationship("Event", backref="host", lazy="dynamic")

    # functions/methods
    def __repr__(self):
        return f"Campaign('{self.name}', '{self.events}')"
####################################################################

####################################################################
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    # relationships - many to many - association tables
    events = db.relationship("Event", 
                             secondary=event_tags, 
                             back_populates="tags")

    organizations = db.relationship("Organization", 
                                    secondary=org_tags, 
                                    back_populates="tags")

    users = db.relationship("User", 
                            secondary=user_tags, 
                            back_populates="tags")
####################################################################
